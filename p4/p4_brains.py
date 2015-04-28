import random

# EXAMPLE STATE MACHINE
class MantisBrain:
    def __init__(self, body):
        self.body = body
        self.state = 'idle'
        self.target = None

    def handle_event(self, message, details):
        if self.state is 'idle':
            if message == 'timer':
                # go to a random point, wake up sometime in the next 10 seconds
                world = self.body.world
                x, y = random.random()*world.width, random.random()*world.height
                self.body.go_to((x,y))
                self.body.set_alarm(random.random()*10)
            elif message == 'collide' and details['what'] == 'Slug':
                # a slug bumped into us; get curious
                self.state = 'curious'
                self.body.set_alarm(1) # think about this for a sec
                self.body.stop()
                self.target = details['who']
        elif self.state == 'curious':
            if message == 'timer':
                # chase down that slug who bumped into us
                if self.target:
                    if random.random() < 0.5:
                        self.body.stop()
                        self.state = 'idle'
                else:
                        self.body.follow(self.target)
                        self.body.set_alarm(1)
            elif message == 'collide' and details['what'] == 'Slug':
                # we meet again!
                slug = details['who']
                slug.amount -= 0.01 # take a tiny little bite

class SlugBrain:
    def __init__(self, body):
        self.body = body
        self.state = 'idle'
        self.target = None
        self.has_resource = False

    def handle_event(self, message, details):
        if self.state is 'idle':
            if message == 'timer':
                if self.body.amount < 0.5:
                    self.state = 'flee'
                    # self.body.set_alarm(1)
                else:
                    # go to a random point, wake up sometime in the next 10 seconds
                    world = self.body.world
                    x, y = random.random()*world.width, random.random()*world.height
                    self.body.go_to((x,y))
                    self.body.set_alarm(random.random()*10)
            elif message == 'collide' and details['what'] == 'Mantis':
                self.target = details['who']
                self.state = 'attack'
                # self.body.set_alarm(1)
            elif message == 'order' and type(details) == tuple:
                self.target = details
                self.state = 'move'
                # self.body.set_alarm(1)
            elif message == 'order':
                if details == 'a':
                    self.state = 'attack'
                    # self.body.set_alarm(1)
                elif details == 'h':
                    self.state = 'harvest'
                    # self.body.set_alarm(1)
                elif details == 'b':
                    self.state = 'build'
            self.body.set_alarm(1)
        elif self.state is 'move':
            if message == 'timer':
                if self.body.amount < 0.5:
                    self.state = 'flee'
                    # self.body.set_alarm(1)
                elif self.target:
                    self.body.go_to(self.target)
                    # self.body.set_alarm(1)
                else:
                    self.state = 'idle'
                    # self.body.set_alarm(1)
            elif message == 'collide' and details['what'] == 'Mantis':
                self.target = details['who']
                self.state = 'attack'
                # self.body.set_alarm(1)
            elif message == 'order' and type(details) == tuple:
                self.target = details
                # self.body.set_alarm(1)
            elif message == 'order':
                if details == 'i':
                    self.body.stop()
                    self.state = 'idle'
                elif details == 'a':
                    self.state = 'attack'
                    # self.body.set_alarm(1)
                elif details == 'h':
                    self.state = 'harvest'
                    # self.body.set_alarm(1)
                elif details == 'b':
                    self.state = 'build'
            self.body.set_alarm(1)
        elif self.state is 'attack':
            if message == 'timer':
                if self.body.amount < 0.5:
                    self.state = 'flee'
                    # self.body.set_alarm(1)
                elif self.target and type(self.target) != tuple:
                    self.body.follow(self.target)
                    # self.body.set_alarm(1)
                else:
                    self.body.follow(self.body.find_nearest('Mantis'))
                    # self.body.set_alarm(1)
            elif message == 'collide' and details['what'] == 'Mantis':
                mantis = details['who']
                mantis.amount -= 0.05
                # self.body.set_alarm(1)
            elif message == 'order' and type(details) == tuple:
                self.target = details
                self.state = 'move'
                # self.body.set_alarm(1)
            elif message == 'order':
                if details == 'i':
                    self.body.stop()
                    self.state = 'idle'
                elif details == 'h':
                    self.state = 'harvest'
                    # self.body.set_alarm(1)
                elif details == 'b':
                    self.state = 'build'
            self.body.set_alarm(1)
        elif self.state is 'harvest':
            if message == 'timer':
                if self.body.amount < 0.5:
                    self.state = 'flee'
                    # self.body.set_alarm(1)
                elif self.has_resource:
                    neartest = self.body.find_nearest('Nest')

                    if neartest:
                        self.body.go_to(neartest)
                    # self.body.set_alarm(1)
                else:
                    neartest = self.body.find_nearest('Resource')

                    if neartest:
                        self.body.go_to(neartest)
                    # self.body.set_alarm(1)
            elif message == 'collide' and details['what'] == 'Resource' and self.has_resource == False:
                resource = details['who']
                resource.amount -= 0.25
                self.has_resource = True
                # self.body.set_alarm(1)
            elif message == 'collide' and details['what'] == 'Nest' and self.has_resource:
                self.has_resource = False
                # self.body.set_alarm(1)
            elif message == 'order' and type(details) == tuple:
                self.target = details
                self.state = 'move'
                # self.body.set_alarm(1)
            elif message == 'order':
                if details == 'i':
                    self.body.stop()
                    self.state = 'idle'
                elif details == 'a':
                    self.state = 'attack'
                    # self.body.set_alarm(1)
                elif details == 'h':
                    self.state = 'harvest'
            self.body.set_alarm(1)
        elif self.state is 'build':
            if message == 'timer':
                if self.body.amount < 0.5:
                    self.state = 'flee'
                    # self.body.set_alarm(1)
                else:
                    neartest = self.body.find_nearest('Nest')

                    if neartest:
                        self.body.go_to(neartest)
            if message == 'collide' and details['what'] == 'Nest':
                nest = details['who']
                nest.amount += 0.01
            elif message == 'order' and type(details) == tuple:
                self.target = details
                self.state = 'move'
                # self.body.set_alarm(1)
            elif message == 'order':
                if details == 'i':
                    self.body.stop()
                    self.state = 'idle'
                elif details == 'a':
                    self.state = 'attack'
                    # self.body.set_alarm(1)
                elif details == 'h':
                    self.state = 'harvest'
                    # self.body.set_alarm(1)
            self.body.set_alarm(1)
        elif self.state is 'flee':
            if message == 'timer':
                self.body.go_to(self.body.find_nearest('Nest'))
                # self.body.set_alarm(1)
            if message == 'collide' and details['what'] == 'Nest':
                self.body.amount += 0.01
            elif message == 'order' and type(details) == tuple:
                self.target = details
                self.state = 'move'
                # self.body.set_alarm(1)
            elif message == 'order':
                if details == 'i':
                    self.body.stop()
                    self.state = 'idle'
                elif details == 'a':
                    self.state = 'attack'
                    # self.body.set_alarm(1)
                elif details == 'h':
                    self.state = 'harvest'
                    # self.body.set_alarm(1)
                elif details == 'b':
                    self.state = 'build'
        self.body.set_alarm(1)

world_specification = {
    # 'worldgen_seed': 13, # comment-out to randomize
    'nests': 3,
    'obstacles': 0,
    'resources': 10,
    'slugs': 5,
    'mantises': 5,
}

brain_classes = {
    'mantis': MantisBrain,
    'slug': SlugBrain,
}
