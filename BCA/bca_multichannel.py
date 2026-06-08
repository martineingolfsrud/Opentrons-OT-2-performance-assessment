#OCT 2025
# in this code, I am attempting to make the robot do a bca assay if i provide it with the right reagents and samples
# I am using the opentrons API to do this
from opentrons import protocol_api

metadata = {
    'protocolName': 'BCA Assay Multichannel',
    'description': '''This protocol performs a simple BCA assay with no unknowns.
                        IMPORTANT: load the standards downwards, A in A1, B in B1, etc.''',
    'author': 'Martine'
}

requirements = {"robotType": "OT-2", "apiLevel": "2.24"} 

def add_parameters(parameters: protocol_api.ParameterContext):

    parameters.add_int(display_name='Number of replicates', variable_name='num_replicates', default=3, minimum=1, maximum=8,
                        description='Number of replicates (1-8)')
    well_plate = [{'display_name': 'A1', 'value': '0'}, {'display_name': 'B1', 'value': '1'}, {'display_name': 'C1', 'value': '2'}, {'display_name': 'D1', 'value': '3'},
                    {'display_name': 'E1', 'value': '4'}, {'display_name': 'F1', 'value': '5'}, {'display_name': 'G1', 'value': '6'}, {'display_name': 'H1', 'value': '7'},
                    {'display_name': 'A2', 'value': '8'}, {'display_name': 'B2', 'value': '9'}, {'display_name': 'C2', 'value': '10'}, {'display_name': 'D2', 'value': '11'},
                    {'display_name': 'E2', 'value': '12'}, {'display_name': 'F2', 'value': '13'}, {'display_name': 'G2', 'value': '14'}, {'display_name': 'H2', 'value': '15'},
                    {'display_name': 'A3', 'value': '16'}, {'display_name': 'B3', 'value': '17'}, {'display_name': 'C3', 'value': '18'}, {'display_name': 'D3', 'value': '19'},
                    {'display_name': 'E3', 'value': '20'}, {'display_name': 'F3', 'value': '21'}, {'display_name': 'G3', 'value': '22'}, {'display_name': 'H3', 'value': '23'},
                    {'display_name': 'A4', 'value': '24'}, {'display_name': 'B4', 'value': '25'}, {'display_name': 'C4', 'value': '26'}, {'display_name': 'D4', 'value': '27'},
                    {'display_name': 'E4', 'value': '28'}, {'display_name': 'F4', 'value': '29'}, {'display_name': 'G4', 'value': '30'}, {'display_name': 'H4', 'value': '31'},
                    {'display_name': 'A5', 'value': '32'}, {'display_name': 'B5', 'value': '33'}, {'display_name': 'C5', 'value': '34'}, {'display_name': 'D5', 'value': '35'},
                    {'display_name': 'E5', 'value': '36'}, {'display_name': 'F5', 'value': '37'}, {'display_name': 'G5', 'value': '38'}, {'display_name': 'H5', 'value': '39'},
                    {'display_name': 'A6', 'value': '40'}, {'display_name': 'B6', 'value': '41'}, {'display_name': 'C6', 'value': '42'}, {'display_name': 'D6', 'value': '43'},
                    {'display_name': 'E6', 'value': '44'}, {'display_name': 'F6', 'value': '45'}, {'display_name': 'G6', 'value': '46'}, {'display_name': 'H6', 'value': '47'},
                    {'display_name': 'E7', 'value': '52'}, {'display_name': 'F7', 'value': '53'}, {'display_name': 'G7', 'value': '54'}, {'display_name': 'H7', 'value': '55'},
                    {'display_name': 'A8', 'value': '56'}, {'display_name': 'B8', 'value': '57'}, {'display_name': 'C8', 'value': '58'}, {'display_name': 'D8', 'value': '59'},
                    {'display_name': 'E8', 'value': '60'}, {'display_name': 'F8', 'value': '61'}, {'display_name': 'G8', 'value': '62'}, {'display_name': 'H8', 'value': '63'},
                    {'display_name': 'A9', 'value': '64'}, {'display_name': 'B9', 'value': '65'}, {'display_name': 'C9', 'value': '66'}, {'display_name': 'D9', 'value': '67'},
                    {'display_name': 'E9', 'value': '68'}, {'display_name': 'F9', 'value': '69'}, {'display_name': 'G9', 'value': '70'}, {'display_name': 'H9', 'value': '71'},
                    {'display_name': 'A10', 'value': '72'}, {'display_name': 'B10', 'value': '73'}, {'display_name': 'C10', 'value': '74'}, {'display_name': 'D10', 'value': '75'},
                    {'display_name': 'E10', 'value': '76'}, {'display_name': 'F10', 'value': '77'}, {'display_name': 'G10', 'value': '78'}, {'display_name': 'H10', 'value': '79'},
                    {'display_name': 'A11', 'value': '80'}, {'display_name': 'B11', 'value': '81'}, {'display_name': 'C11', 'value': '82'}, {'display_name': 'D11', 'value': '83'},
                    {'display_name': 'E11', 'value': '84'}, {'display_name': 'F11', 'value': '85'}, {'display_name': 'G11', 'value': '86'}, {'display_name': 'H11', 'value': '87'},
                    {'display_name': 'A12', 'value': '88'}, {'display_name': 'B12', 'value': '89'}, {'display_name': 'C12', 'value': '90'}, {'display_name': 'D12', 'value': '91'},
                    {'display_name': 'E12', 'value': '92'}, {'display_name': 'F12', 'value': '93'}, {'display_name': 'G12', 'value': '94'}, {'display_name': 'H12', 'value': '95'}
                ]
    cols = [{'display_name': '1', 'value': '0'}, {'display_name': '2', 'value': '1'}, {'display_name': '3', 'value': '2'},
            {'display_name': '4', 'value': '3'}, {'display_name': '5', 'value': '4'}, {'display_name': '6', 'value': '5'},
            {'display_name': '7', 'value': '6'}, {'display_name': '8', 'value': '7'}, {'display_name': '9', 'value': '8'},
            {'display_name': '10', 'value': '9'}, {'display_name': '11', 'value': '10'}, {'display_name': '12', 'value': '11'}]
    
    # starting tip for the 300 uL pipette
    parameters.add_str(display_name = 'Starting Tip 300 uL', variable_name = 'start_tip_300', default = '0', choices = well_plate)
    #starting col for the 8 channel pipette
    parameters.add_str(display_name = 'Starting Column 8-Channel', variable_name = 'start_col_8', default = '0', choices = cols)

def run(protocol: protocol_api.ProtocolContext):
    # ----------- LABWARE AND PIPETTES -----------
    standards = protocol.load_labware('opentrons_24_tuberack_eppendorf_2ml_safelock_snapcap', 4)
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 5)
    reservoir = protocol.load_labware('opentrons_tough_12_reservoir_22ml', 6)

    single_tips = protocol.load_labware('opentrons_96_tiprack_300ul', 10)
    multi_tips = protocol.load_labware('opentrons_96_tiprack_300ul', 11)

    p300_single = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[single_tips])
    p300_multi = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=[multi_tips])
    p300_single.starting_tip = single_tips.wells()[int(protocol.params.start_tip_300)]
    p300_multi.starting_tip = multi_tips.wells()[int(protocol.params.start_col_8)*8]

    #******** this is 'actual' code ********

    replicates = protocol.params.num_replicates
    
    protocol.comment('Adding standards to all wells')
        # intended functionality: pik up pipette tip - transfer all instances of A to column 1,
        # then drop tip, pick up new tip, transfer all instances of B to column 2, etc.
    for i in range(9):
        p300_single.pick_up_tip()
        for repl in range(replicates):
            source = standards.wells()[i]
            dest = plate.rows()[repl][i]
            p300_single.transfer(25, source, dest, new_tip='never')
        p300_single.drop_tip()    
    
    protocol.comment('Adding working reagent to all wells')
    p300_multi.transfer(200, reservoir['A1'], plate.rows()[0][0:9], new_tip='always', mix_after=(3,150))

    protocol.pause('Incubate the plate at 37C for 30 minutes, then read absorbance at 562 nm.')
    protocol.comment('Protocol complete.')

#D8AEC8
#D88F8F