# over-engineered time dial
class TimeDial:
    """
    Time dial with two regimes:
      - inside circle: geometric mapping from 0..inner_cap
      - outside circle: momentum-driven motion starting from anchor_seconds

    Constructor:
        TimeDial(anchor_seconds: int)
    """
    def __init__(self, anchor_seconds: int):
        self.anchor_seconds = int(anchor_seconds) if anchor_seconds is not None else int(360 * 24 * 3600)

        self.true_seconds = 0.0

        # momentum / outside state
        self.outside_time = 0.0
        self.momentum = 0.0
        self.decay = 0.995
        self.threshold = 0.2

        # direction detection
        self.last_direction = 0
        self.direction_timer = 0.0
        self.direction_delay = 0.2
        self.pending_direction = 0

        self.prev_outside = 0.0
        self.anchor_locked = False   # becomes True once user first crosses outside boundary
        
        self.milestones = [
            3600,
            86400,
            365 * 86400
        ]

    def update(self, raw_distance: float, max_radius: float, dt: float) -> int:
        """
        raw_distance: distance from center to pointer
        max_radius: radius of inner dial (geometry)
        dt: delta time seconds since last update
        returns: int true_seconds
        """
        HOUR = 3600.0
        DAY = 86400

        outside = raw_distance - max_radius

        inner_cap = min(self.anchor_seconds, HOUR)
        # --- INSIDE: precision zone, geometry to time
        if outside <= 0:
            self.outside_time = 0.0
            self.momentum = 0.0
            self.last_direction = 0
            self.direction_timer = 0.0
            self.prev_outside = outside

            t = max(0.0, min(raw_distance / max_radius if max_radius > 0 else 0.0, 1.0))


            if self.true_seconds <= inner_cap:
                self.true_seconds = inner_cap * (t ** 1.2)
            else: #caps
                self.true_seconds = inner_cap


            # round up
            if self.true_seconds >= HOUR:
                return int(self.true_seconds // 60 * 60)
            else:
                return int(self.true_seconds)
        
        if inner_cap == self.anchor_seconds:
            return int(self.true_seconds)

        # --- OUTSIDE: momentum-driven, anchored
        # lock anchor the first time we go outside
        if not self.anchor_locked:
            # either snap to anchor_seconds, or ensure baseline not below anchor
            self.true_seconds = max(self.true_seconds, inner_cap)
            self.anchor_locked = True
            self.outside_time = 0.0
            # don't reset prev_outside here — keep it to measure delta this frame

        # accumulate outside time (patience)
        self.outside_time += dt

        # intent detection
        delta = outside - self.prev_outside
        self.prev_outside = outside

        raw_direction = 0
        if delta > self.threshold:
            raw_direction = 1
        elif delta < -self.threshold:
            raw_direction = -1

        # hard stop: opposing momentum kills momentum immediately
        # hard stop and hysteresis (replacement block)
        effective_direction = 0

        # === DIRECTION BRAKE + DELAY ===
        if self.pending_direction != 0:
            # user backed off or returned to previous direction → cancel
            if raw_direction == 0 or raw_direction == self.last_direction:
                self.pending_direction = 0
                self.direction_timer = 0.0
            else:
                # user is still opposing → wait
                self.direction_timer += dt
                if self.direction_timer >= self.direction_delay:
                    self.last_direction = self.pending_direction
                    self.pending_direction = 0
                    self.direction_timer = 0.0
            # HARD STOP while waiting
            self.momentum = 0.0
            
            # round up
            if self.true_seconds >= HOUR:
                return int(self.true_seconds // 60 * 60)
            else:
                return int(self.true_seconds)

        # === NO PENDING: HANDLE INPUT ===
        if raw_direction != 0:
            if self.last_direction == 0:
                self.last_direction = raw_direction
                effective_direction = self.last_direction
                self.momentum = 0.0
            elif raw_direction == self.last_direction:
                effective_direction = self.last_direction
            else:
                # opposing input → stop immediately and arm delay
                self.pending_direction = raw_direction
                self.direction_timer = 0.0
                self.momentum = 0.0
                
                # round up
                if self.true_seconds >= HOUR:
                    return int(self.true_seconds // 60 * 60)
                else:
                    return int(self.true_seconds)
        else:
            effective_direction = 0


        # smooth factors
        distance_term = max(0.0, outside) ** 1.2
        time_term = (self.outside_time) ** 1.3

        # acceleration rules
        if effective_direction == 0:
            self.momentum *= self.decay
            if abs(self.momentum) < 0.01:
                self.momentum = 0.0
        else:
            acceleration = effective_direction * (1.0 + distance_term * 0.02 + time_term * 3.0)
            self.momentum += acceleration

        # integrate momentum into seconds
        self.true_seconds += self.momentum * dt * 100.0

        # clamp to allowed range
        self.true_seconds = max(0.0, min(self.true_seconds, float(self.anchor_seconds)))
        
        for m in self.milestones:
            if abs(self.true_seconds - m) < m * 0.015:
                self.true_seconds = m
                self.momentum *= 0.4
                break
        
        if self.true_seconds >= HOUR:
            # round to whole minutes
            return int(self.true_seconds // 60 * 60)
        else:
            return int(self.true_seconds)
        