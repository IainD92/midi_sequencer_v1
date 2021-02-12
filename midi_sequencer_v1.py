# midi_sequencer_v1
#this needs compiled to cython to run anywhere near fast enough to be usuable in a musical context
import time

#not using patch parameter automation yet...
#from midi_master_patcher import*


#Step - holds note data for a subdivision in the music (trigger, velocity, gate, tie)
class Step:
    def __init__(self):
        self.trigger = False
        self.velocity = 96
        self.gate = 0.5
        self.tie = False
        
    def setTrigger(self, trigger):
        if trigger == True:
            self.trigger = trigger
        elif trigger == False:
            self.trigger = trigger
        else:
            print("error! setTrigger takes bool values")
    
    def setVelocity(self, velocity):
        self.velocity = velocity
        
    def setGate(self, gate):
        self.gate = gate
        
    def setTie(self, tie):
        if tie == True:
            self.tie = tie
        elif tie == False:
            self.tie = tie
        else:
            print("error! setTie takes bool values")
        

#mono step sequencer - holds Step() objects in an array (bars*subdivisions)
class midiSequencer:
    #initialise variables
    def __init__ (self, name, bars, subdivisions):
        self.name = name
        self.bars = bars
        self.subdivisions = subdivisions
        
        #set up variables for calculating time
        self.tempo = 135.5
        self.tickLength = ((60/self.tempo)*4)/self.subdivisions #duraton of bar in seconds, divided by subdivisions
        self.t_firstTick = 0.1
        self.t_nextTick = 0.1
        self.nextTick = 0
        self.activeBar = 0
        
        #set up a nested list of subdivisions, in bars. fill subdivisions with Step() objects
            #takes the format barsSteps[bars][steps], where barsSteps[0][0] is the first step of the first bar
        self.barsSteps = [[Step()]*subdivisions for i in range(bars)]


    #methods for editing step parameters
        #these just pass the parameter to the relavent Step object via the appropriate method
    def setTrigger(self, bar, step, trigger):
            self.barsSteps[bar][step].setTrigger(trigger)
    def setVelocity(self, bar, step, velocity):
            self.barsSteps[bar][step].setVelocity(velocity)
    def setGate(self, bar, step, gate):
            self.barsSteps[bar][step].setGate(gate)
    def setTie(self, bar, step, tie):
            self.barsSteps[bar][step].setTie(tie)

    #methods for clock / time management
            #whats the current step, when is the next one supposed to be, etc
    #edit the tempo (and calculate time between ticks)
    def set_tempo(self, tempo):
        self.tempo = tempo
        self.tickLength = ((60/self.tempo)*4)/self.subdivisions #duraton of bar in seconds, divided by subdivisions
        
    #start the sequencer
    def start(self, tempo):
        self.set_tempo(tempo)
        self.t_firstTick = time.process_time()
        self.t_nextTick = self.t_firstTick
        self.nextStep = 0
        self.activeBar = 0
    
    #play the step, and work out when/what the next one is
    def update(self):
        print(self.name,"- |bar",self.activeBar,"|step", self.nextStep, "|Trigger:", self.barsSteps[self.activeBar][self.nextTick].trigger, " |Velocity:", self.barsSteps[self.activeBar][self.nextTick].velocity, " |Gate:", self.barsSteps[self.activeBar][self.nextTick].gate)
        self.t_nextTick += self.tickLength
        self.nextStep +=1
        if self.nextStep >= self.subdivisions:
            self.nextStep = 0
            self.activeBar += 1           
        if self.activeBar >= self.bars:
            self.activeBar = 0 #back to the start

        
        
        
        
#test clock

#initialise
seq1=midiSequencer("seq1",64,16)
seq2=midiSequencer("seq2",64,16)
seq3=midiSequencer("seq3",64,16)
seq4=midiSequencer("seq4",64,16)
seq5=midiSequencer("seq5",64,16)
seq6=midiSequencer("seq6",64,16)
seq7=midiSequencer("seq7",64,16)
seq8=midiSequencer("seq8",64,16)
seq9=midiSequencer("seq9",64,16)

seq10=midiSequencer("seq10",64,16)
seq11=midiSequencer("seq11",64,16)
seq12=midiSequencer("seq12",64,16)
seq13=midiSequencer("seq13",64,16)
seq14=midiSequencer("seq14",64,16)

sequencers = [seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8, seq9, seq10, seq11, seq12, seq13, seq14]

for s in sequencers:
    s.start(140)

t_current = time.process_time()

#loop forever
while True:
    t_current = time.process_time()
    
    for s in sequencers:    
        if t_current >= s.t_nextTick:
            s.update()
    
