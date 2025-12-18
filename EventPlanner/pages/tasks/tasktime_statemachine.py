import math

class TimeDial:
    """
    Time dial with two regimes:
      - inside circle: geometric mapping from 0..inner_scale_seconds
      - outside circle: momentum-driven motion starting from anchor_seconds

    Constructor:
        TimeDial(max_seconds: int,
                 anchor_seconds: int,
                 inner_scale_seconds: int)
    """
    def __init__(self, max_seconds: int, anchor_seconds: int, inner_scale_seconds: int):
        self.max_seconds = int(max_seconds)
        self.anchor_seconds = int(anchor_seconds) if anchor_seconds is not None else int(inner_scale_seconds)
        self.inner_scale_seconds = int(inner_scale_seconds)

        self.true_seconds = 0.0

        # momentum / outside state
        self.outside_time = 0.0
        self.momentum = 0.0
        self.decay = 0.995
        self.threshold = 0.001

        # direction detection
        self.last_direction = 0
        self.direction_timer = 0.0
        self.direction_delay = 0.1

        self.prev_outside = 0.0
        self.anchor_locked = False   # becomes True once user first crosses outside boundary

    def update(self, raw_distance: float, max_radius: float, dt: float) -> int:
        """
        raw_distance: distance from center to pointer
        max_radius: radius of inner dial (geometry)
        dt: delta time seconds since last update
        returns: int true_seconds
        """
        outside = raw_distance - max_radius

        # --- INSIDE: geometry maps to [0 .. inner_scale_seconds]
        if outside <= 0:
            # reset outside/momentum state
            self.outside_time = 0.0
            self.momentum = 0.0
            self.last_direction = 0
            self.direction_timer = 0.0
            self.prev_outside = outside
            self.anchor_locked = False

            # geometric mapping (non-linear)
            t = max(0.0, min(raw_distance / max_radius if max_radius > 0 else 0.0, 1.0))
            self.true_seconds = float(self.inner_scale_seconds) * (t ** 1.4)
            return int(self.true_seconds)

        # --- OUTSIDE: momentum-driven, anchored
        # lock anchor the first time we go outside
        if not self.anchor_locked:
            # either snap to anchor_seconds, or ensure baseline not below anchor
            self.true_seconds = max(self.true_seconds, float(self.anchor_seconds))
            self.anchor_locked = True
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
        if raw_direction != 0 and self.momentum != 0:
            if raw_direction != int(math.copysign(1, self.momentum)):
                self.momentum = 0.0
                self.last_direction = raw_direction
                self.direction_timer = 0.0

        # direction hysteresis
        if self.last_direction == 0 and abs(raw_direction) == 1:
            self.last_direction = raw_direction
            self.direction_timer = 0.0
            effective_direction = self.last_direction
        elif raw_direction == self.last_direction or raw_direction == 0:
            effective_direction = self.last_direction
        else:
            # direction changed; wait briefly
            self.direction_timer += dt
            if self.direction_timer >= self.direction_delay:
                self.direction_timer = 0.0
                self.last_direction = raw_direction
                effective_direction = self.last_direction
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
        # scale factor 100 is preserved from your original code
        self.true_seconds += self.momentum * dt * 100.0

        # clamp to allowed range
        self.true_seconds = max(0.0, min(self.true_seconds, float(self.max_seconds)))
        return int(self.true_seconds)