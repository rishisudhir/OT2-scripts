from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Serial Dilution - 10x',
}

def run(protocol: protocol_api.ProtocolContext):
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
    tiprack2 = protocol.load_labware('opentrons_96_tiprack_20ul', 4)

    reservoir = protocol.load_labware('nest_1_reservoir_195ml', 2)
    plate = protocol.load_labware('nest_96_wellplate_200ul_flat', 3)
    
    p300 = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=[tiprack])
    p20 = protocol.load_instrument('p20_multi_gen2', 'right', tip_racks=[tiprack2])
    
    # distribute diluent starting from the second column
    p300.pick_up_tip()
    p300.transfer(180, reservoir['A1'], plate.columns()[1:],new_tip='never')
    p300.return_tip()


    # save the destination row to a variable
    row = plate.rows()[0]

    # dilute the sample down the row
    for source, destination in zip(row[:10], row[1:11]):
        p20.pick_up_tip()  # Pick up a new tip before each transfer
        p20.transfer(20, source, destination, mix_after=(1, 20), new_tip='never')
        p20.blow_out(destination.bottom())
        p20.drop_tip()  # Drop the tip after each transfer

    # Pick up 20 µl from the 11th well and discard the tip
    p300.pick_up_tip()
    p300.aspirate(20, row[10])
    p300.drop_tip()
 
