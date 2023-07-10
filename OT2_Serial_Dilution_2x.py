# Script name: OT2 Serial Dilution - 2x.py
# Directory path: cd C:\Users\Rishi\YOUR DIRECTORY GOES HERE
# Command line simulation = opentrons_simulate.exe OT2_Serial_Dilution_2x.py -e

from opentrons import protocol_api
from opentrons import types

metadata = {
    'apiLevel': '2.8',
    'protocolName': 'Serial Dilution - 2x',
}

def run(protocol: protocol_api.ProtocolContext):
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
    #tiprack2 = protocol.load_labware('opentrons_96_tiprack_300ul', 4)
    reservoir = protocol.load_labware('nest_1_reservoir_195ml', 2)
    plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 3)
    p300 = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=[tiprack])

    # distribute diluent starting from the second column
    p300.pick_up_tip()
    p300.transfer(200, reservoir['A1'], plate.columns()[1:],new_tip='never')
    p300.return_tip()


    # save the destination row to a variable
    row = plate.rows()[0]

    # set the flowrate to default; change it here for future reference
    p300.flow_rate.aspirate = 94 # default for 94ul/sec
    p300.flow_rate.dispense = 94 # default for 94ul/sec

    # dilute the sample across the columns, left to right
    for source, destination in zip(row[:10], row[1:11]):
        p300.pick_up_tip()  # Pick up a new tip before each transfer
        p300.transfer(100, source, destination.bottom(3.0), mix_after=(1, 100), new_tip='never')
        p300.blow_out(destination.bottom(3.0))
        p300.drop_tip()  # Drop the tip after each transfer

    # Pick up 100 µl from the 11th well and discard the tip
    p300.pick_up_tip()
    p300.aspirate(100, row[10])
    p300.drop_tip()
 
