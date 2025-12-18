import math

class TimeDial:
    def __init__(self, max_seconds, anchor_seconds):
        self.max_seconds = max_seconds
        self.anchor_seconds = anchor_seconds
        
        self.true_seconds = 0
        
        self.outside_distance = 0.0
        self.outside_time = 0.0
        self.momentum = 0.0
        self.decay = 0.995
        self.threshold = 0.001 # threshold before deciding to move
        
        self.last_direction = 0        # -1, 0, +1
        self.direction_timer = 0.0     # how long we've been unsure
        self.direction_delay = 0.1     # how long is the temporal unsureness gonna last

        self.prev_outside = 0.0
        
    def update(self, raw_distance, max_radius, dt):
        # magnitude: mouse to bounds vector
        outside = raw_distance - max_radius
        
        # inside dial: geometry owns time
        if outside <= 0:
            self.outside_time = 0
            self.momentum = 0           # stop momentum and switch to geometric scaling time
            self.last_direction = 0
            self.direction_timer = 0
            self.prev_outside = outside
            
            t = raw_distance / max_radius
            self.true_seconds = int(self.anchor_seconds * (t ** 1.4))
            return int(self.true_seconds)
            
        # outside dial: momentum owns time (after 1 year)
        # seconds elapsed
        self.outside_time += dt
        
        # intent detection: 3 states: pulling outwards, hessitating, pulling inwards
        delta = outside - self.prev_outside
        self.prev_outside = outside # calculate distance from last location and storing it, then renew position next update

        # normal = 1, hessitate = 0, decrease = 1 
        raw_direction = 0
        if delta > self.threshold:
            raw_direction = 1
        elif delta < -self.threshold:
            raw_direction = -1
            
        # HARD STOP: kill opposing momentum #! why need to go the -1 way 2 times in a row to stop
        if raw_direction != 0 and self.momentum != 0:
            if raw_direction != int(math.copysign(1, self.momentum)):
                self.momentum = 0
                self.last_direction = raw_direction
                self.direction_timer = 0

        if self.last_direction == 0 and abs(raw_direction) == 1:  # newest workable direction
            self.last_direction = raw_direction
            self.direction_timer = 0
            effective_direction = self.last_direction
        elif raw_direction == self.last_direction or raw_direction == 0:  # last direction is the same as the current direction, or no raw direction
            effective_direction = self.last_direction
        else:
            # direction changed, start wait
            self.direction_timer += dt #! if assigned, need to jam everything else
            if self.direction_timer >= self.direction_delay:
                # ok, user really mean it
                self.direction_timer = 0
                self.last_direction = raw_direction
                effective_direction = self.last_direction
            else:
                # still hessitating
                effective_direction = 0
        
        # smooth curves mmm
        distance_term = outside ** 1.2
        time_term = self.outside_time ** 1.3
        
        # how fast time moves: direction * (Base speed + distance influence + patience influence), time always moves by 1 second outside dial
        if effective_direction == 0:
            # hold and coast with same less momentum over time
            self.momentum *= self.decay
            
            # snap momentum to zero
            if effective_direction == 0 and abs(self.momentum) < 0.01:
                self.momentum = 0
        elif effective_direction == -1:
            # pull-back, stop momentum and go into hessitation
            acceleration = effective_direction * (1 + distance_term * 0.02 + time_term * 3)
            self.momentum += acceleration

        else:
            # push any direction after that = accelerate that direction
            acceleration = effective_direction * (1 + distance_term * 0.02 + time_term * 3) # direction * speed
            self.momentum += acceleration

        print(self.momentum)
        # convert direction and wait to true time
        self.true_seconds += self.momentum * dt * 100
        self.true_seconds = max(0, min(self.true_seconds, self.max_seconds)) # never < 0, never more than max_seconds
        return int(self.true_seconds)