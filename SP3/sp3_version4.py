# ATTEMPT 4 at building the sp3 protocol step by step it will begin as an improved copy of katarinas sp3_v3 but not be hard-coded
# but instead utilize the parameter functionality to make it more flexible
from opentrons import protocol_api
from opentrons.types import Point

metadata = {
    'protocolName': 'SP3 Sample Preparation v4.0',
    'description': '''This protocol performs SP3 sample preparation including protein binding, washing, and digestion steps.''',
    'author': 'Martine'
}

requirements = {"robotType": "OT-2", "apiLevel": "2.24"} #2.24 is the latest api level as of september 2025

def add_parameters(parameters: protocol_api.ParameterContext):
    # ------------- Parameters that can be adjusted by the user -------------
    # number of samples to process
    parameters.add_int(display_name = 'Number of Samples', variable_name='num_samples', default = 1, 
                        description='Number of samples to process. Max 96.', minimum=1, maximum=96)
    # volume of each sample
    parameters.add_float(display_name='Sample Volume', variable_name='sample_vol', default = 50.0,
                        description='Volume of each sample in uL.',  unit='uL', minimum = 20.0, maximum = 70.0)
    # number of replicates
    parameters.add_int(display_name = 'Number of Replicates', variable_name='num_replicates', default = 1, 
                        description='Number of replicates per sample. Max 4.', minimum=1, maximum=4)
    # volume of beads to add to each sample
    parameters.add_float(display_name='Bead Volume (each sample)', variable_name='bead_vol', default = 2.5,
                        description='Volume of beads to add to each sample in uL.',  unit='uL', minimum = 1.0, maximum = 10.0)
    # volume of 80% ethanol to add to each sample for washing
    parameters.add_float(display_name='80% Ethanol Volume', variable_name='etoh80_vol', default = 180.0,
                        description='Volume of 80% ethanol to add to each sample in uL for washing.',  unit='uL', minimum = 100.0, maximum = 300.0)
    
    well_plate = [
    {'display_name': 'A1', 'value': '0'}, {'display_name': 'A2', 'value': '8'}, {'display_name': 'A3', 'value': '16'},
    {'display_name': 'A4', 'value': '24'}, {'display_name': 'A5', 'value': '32'}, {'display_name': 'A6', 'value': '40'},
    {'display_name': 'A7', 'value': '48'}, {'display_name': 'A8', 'value': '56'}, {'display_name': 'A9', 'value': '64'},
    {'display_name': 'A10', 'value': '72'}, {'display_name': 'A11', 'value': '80'}, {'display_name': 'A12', 'value': '88'},
    {'display_name': 'B1', 'value': '1'}, {'display_name': 'B2', 'value': '9'}, {'display_name': 'B3', 'value': '17'},
    {'display_name': 'B4', 'value': '25'}, {'display_name': 'B5', 'value': '33'}, {'display_name': 'B6', 'value': '41'},
    {'display_name': 'B7', 'value': '49'}, {'display_name': 'B8', 'value': '57'}, {'display_name': 'B9', 'value': '65'},
    {'display_name': 'B10', 'value': '73'}, {'display_name': 'B11', 'value': '81'}, {'display_name': 'B12', 'value': '89'},
    {'display_name': 'C1', 'value': '2'}, {'display_name': 'C2', 'value': '10'}, {'display_name': 'C3', 'value': '18'},
    {'display_name': 'C4', 'value': '26'}, {'display_name': 'C5', 'value': '34'}, {'display_name': 'C6', 'value': '42'},
    {'display_name': 'C7', 'value': '50'}, {'display_name': 'C8', 'value': '58'}, {'display_name': 'C9', 'value': '66'},
    {'display_name': 'C10', 'value': '74'}, {'display_name': 'C11', 'value': '82'}, {'display_name': 'C12', 'value': '90'},
    {'display_name': 'D1', 'value': '3'}, {'display_name': 'D2', 'value': '11'}, {'display_name': 'D3', 'value': '19'},
    {'display_name': 'D4', 'value': '27'}, {'display_name': 'D5', 'value': '35'}, {'display_name': 'D6', 'value': '43'},
    {'display_name': 'D7', 'value': '51'}, {'display_name': 'D8', 'value': '59'}, {'display_name': 'D9', 'value': '67'},
    {'display_name': 'D10', 'value': '75'}, {'display_name': 'D11', 'value': '83'}, {'display_name': 'D12', 'value': '91'},
    {'display_name': 'E1', 'value': '4'}, {'display_name': 'E2', 'value': '12'}, {'display_name': 'E3', 'value': '20'},
    {'display_name': 'E4', 'value': '28'}, {'display_name': 'E5', 'value': '36'}, {'display_name': 'E6', 'value': '44'},
    {'display_name': 'E7', 'value': '52'}, {'display_name': 'E8', 'value': '60'}, {'display_name': 'E9', 'value': '68'},
    {'display_name': 'E10', 'value': '76'}, {'display_name': 'E11', 'value': '84'}, {'display_name': 'E12', 'value': '92'},
    {'display_name': 'F1', 'value': '5'}, {'display_name': 'F2', 'value': '13'}, {'display_name': 'F3', 'value': '21'},
    {'display_name': 'F4', 'value': '29'}, {'display_name': 'F5', 'value': '37'}, {'display_name': 'F6', 'value': '45'},
    {'display_name': 'F7', 'value': '53'}, {'display_name': 'F8', 'value': '61'}, {'display_name': 'F9', 'value': '69'},
    {'display_name': 'F10', 'value': '77'}, {'display_name': 'F11', 'value': '85'}, {'display_name': 'F12', 'value': '93'},
    {'display_name': 'G1', 'value': '6'}, {'display_name': 'G2', 'value': '14'}, {'display_name': 'G3', 'value': '22'},
    {'display_name': 'G4', 'value': '30'}, {'display_name': 'G5', 'value': '38'}, {'display_name': 'G6', 'value': '46'},
    {'display_name': 'G7', 'value': '54'}, {'display_name': 'G8', 'value': '62'}, {'display_name': 'G9', 'value': '70'},
    {'display_name': 'G10', 'value': '78'}, {'display_name': 'G11', 'value': '86'}, {'display_name': 'G12', 'value': '94'},
    {'display_name': 'H1', 'value': '7'}, {'display_name': 'H2', 'value': '15'}, {'display_name': 'H3', 'value': '23'},
    {'display_name': 'H4', 'value': '31'}, {'display_name': 'H5', 'value': '39'}, {'display_name': 'H6', 'value': '47'},
    {'display_name': 'H7', 'value': '55'}, {'display_name': 'H8', 'value': '63'}, {'display_name': 'H9', 'value': '71'},
    {'display_name': 'H10', 'value': '79'}, {'display_name': 'H11', 'value': '87'}, {'display_name': 'H12', 'value': '95'}
]
    tube_rack = [
    {'display_name': 'A1', 'value': '0'}, {'display_name': 'B1', 'value': '1'}, {'display_name': 'C1', 'value': '2'}, {'display_name': 'D1', 'value': '3'},
    {'display_name': 'A2', 'value': '4'}, {'display_name': 'B2', 'value': '5'}, {'display_name': 'C2', 'value': '6'}, {'display_name': 'D2', 'value': '7'},
    {'display_name': 'A3', 'value': '8'}, {'display_name': 'B3', 'value': '9'}, {'display_name': 'C3', 'value': '10'}, {'display_name': 'D3', 'value': '11'},
    {'display_name': 'A4', 'value': '12'}, {'display_name': 'B4', 'value': '13'}, {'display_name': 'C4', 'value': '14'}, {'display_name': 'D4', 'value': '15'},
    {'display_name': 'A5', 'value': '16'}, {'display_name': 'B5', 'value': '17'}, {'display_name': 'C5', 'value': '18'}, {'display_name': 'D5', 'value': '19'},
    {'display_name': 'A6', 'value': '20'}, {'display_name': 'B6', 'value': '21'}, {'display_name': 'C6', 'value': '22'}, {'display_name': 'D6', 'value': '23'}
]

    # starting tip for the 300 uL pipette
    parameters.add_str(display_name = 'Starting Tip 300 uL', variable_name = 'start_tip_300', default = '0', 
                        choices = well_plate)
    # starting tip for the 20 uL pipette
    parameters.add_str(display_name = 'Starting Tip 20 uL', variable_name = 'start_tip_20', default = '0', 
                        choices = well_plate)
    # starting well in sample plate
    parameters.add_str(display_name = 'Starting Sample Well', variable_name = 'start_sample_well', default = '0',
                        choices = well_plate)
    # which well of the reagent plate contains the beads
    #* commenting this one out - we put beads in an eppendorf tube always in A1
    #parameters.add_str(display_name = 'Bead Slot', variable_name = 'bead_well', default = '0', choices = tube_rack)

def run(protocol: protocol_api.ProtocolContext):
    # some variables made from the parameters
    etoh100_vol = (protocol.params.sample_vol/0.3) - protocol.params.sample_vol # volume of 100% ethanol to add to each sample in uL for a final concentration of 70%
    total_samples = int(protocol.params.num_samples) * int(protocol.params.num_replicates) # total number of samples including replicates (to know how many wells are needed)

    # ------------- Labware and Pipette Setup -------------
    tips300 = protocol.load_labware('opentrons_96_tiprack_300ul', 9)
    tips20 = protocol.load_labware('opentrons_96_tiprack_20ul', 6)
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tips300])
    p20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tips20])
    p300.starting_tip = tips300.wells()[int(protocol.params.start_tip_300)]
    p20.starting_tip = tips20.wells()[int(protocol.params.start_tip_20)]

    tuberack = protocol.load_labware('opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', 3)
    magdeck = protocol.load_module('magnetic module', 1)
    if magdeck.status == 'engaged':
        magdeck.disengage()
    magplate = magdeck.load_labware('eppendorf_96_wellplate_500ul')
    reagentplate = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 2)

    # ------------- Reagents Setup -------------
    beads = reagentplate.wells_by_name()['A1'] # beads
    etoh100 = tuberack.wells_by_name()['A1'] # 100% EtOH
    etoh80 = tuberack.wells_by_name()['A2'] # 80% EtOH
    waste = tuberack.wells_by_name()['A3'] # waste container for supernatant


    start_well_index = int(protocol.params.start_sample_well)
    available_wells = 96 - start_well_index
    magwells = magplate.wells()[start_well_index : start_well_index + int(total_samples)]

    #* adding a function to split the magwells into evens and odds here, allows for better handling of bead position in well
    # -------------- SPLIT INTO EVENS AND ODDS --------------
        # this is in order to account for every other column pushing the beads to different sides of the well
    evens = []
    odds = []

    for well in magwells:
        # Extract the column number from the well name
        column_number = int(well.well_name[1:])  # Extract the numeric part of the well name
        if column_number % 2 == 0:  # Check if the column number is even
            evens.append(well)
        else:
            odds.append(well)

    # Debugging: Print the results
    protocol.comment(f"Evens: {[well.well_name for well in evens]}")
    protocol.comment(f"Odds: {[well.well_name for well in odds]}")

    if total_samples > available_wells:
        protocol.pause(f"Not enough wells in the plate starting from {protocol.params.start_sample_well}. Please use a new plate or adjust the number of samples/replicates.")
        raise Exception("Not enough wells in the plate.")

    # ------------- THE ACTUAL PROTOCOL -------------
    protocol.comment('Starting the SP3 protocol!')
    protocol.comment(f'Total samples including replicates: {total_samples}')
    protocol.comment(f'Using wells: {[well.well_name for well in magwells]}')
    protocol.comment(f'Sample volume: {protocol.params.sample_vol} uL')
    protocol.comment(f'Bead volume: {protocol.params.bead_vol} uL')
    protocol.comment(f'80% EtOH volume: {protocol.params.etoh80_vol} uL')
    protocol.comment(f'100% EtOH volume: {etoh100_vol} uL') 

    # STEP 1: add beads to each sample
    protocol.comment('Step 1: Adding beads to each sample')
    
    #* no need to have mixing here, the small volume doesn't allow for it anyway
    #! added blowout - it seems like some sample doesn't come out otherwise and ends up in the trash
    p20.transfer(protocol.params.bead_vol, beads, magwells, new_tip = 'always', blow_out = True, blowout_location = 'destination well')
    
    #* changed bottom from 70 to 60, to ensure etoh pickup for all samples
    #! changed mix_vol - it currently picks up MORE than there is in the well, but multiplying by 0.9 should resolve this
    #! added blowout! turns out the beads can clog the pipette and then two bad things happen - 1: mixing does not occur
    #! 2: it slowly picks up volume, but then dispenses all of it in the trash, because it assumes it is empty
    # STEP 2: add 100% EtOH to each sample for a final concentration of 70%
    protocol.comment('Step 2: Adding 100% EtOH to each sample for a final concentration of 70%')
    mix_vol = (protocol.params.sample_vol + etoh100_vol)*0.9
    p300.transfer(etoh100_vol, etoh100.bottom(40), magwells
                , mix_after = (10, mix_vol if mix_vol < 300 else 300, [well.bottom(1) for well in magwells])
                , new_tip = 'always',
                    blow_out = True, blowout_location = 'destination well') 
    
    # STEP 3 Incubate at 24°C for 7 minutes manually
    protocol.pause('Incubate samples at 24°C for 7 minutes. Click RESUME when done.')
    protocol.comment('Resuming protocol')

    # STEP 4: Engage magnetic module and wait for beads to collect
    protocol.comment('Step 4: Engaging magnetic module and waiting for beads to collect')
    magdeck.engage(height_from_base=5)
    protocol.delay(minutes=5, msg= 'Incubating on magnet for 5 minutes') # wait 5 minutes
    protocol.comment('Beads should now be collected on the magnet.')

    # STEP 5: Remove supernatant after initial incubation
    #* moving the aspiration here to the sides - aka splitting into two commands
    #* the blowout_location was source well, but if there is leftover supernatant i'd want it do be blown out into waste (destination well)
    #! changed new_tip to 'always' to avoid cross-contamination when removing supernatant - it was 'once' before, which worked fine,
    #! but splitting into evens and odds seems to have done something to it - better safe than sorry
    protocol.comment('Step 5: Removing supernatant')
    p300.flow_rate.aspirate = 25  # Slow down aspirate speed to avoid disturbing beads
    if odds != []:
        # odds
        p300.transfer((protocol.params.sample_vol + etoh100_vol *1.1), [well.bottom().move(Point(-2,-2,1)) for well in odds], waste.top(), 
                        new_tip = 'always', air_gap = 10, blow_out = True, blowout_location = 'destination well')
    if evens != []:
        # evens
        p300.transfer((protocol.params.sample_vol + etoh100_vol *1.1), [well.bottom().move(Point(2,-2,1)) for well in evens], waste.top(), 
                        new_tip = 'always', air_gap = 10, blow_out = True, blowout_location = 'destination well')

    # STEP 6: Washing with 80% EtOH
    protocol.comment('Step 6: Washing with 80% EtOH')
    
    #? WASH 1
    for i in range(3):  # Repeat wash 3 times
        p300.flow_rate.aspirate = 94  # Reset to default aspirate speed
        magdeck.disengage()

        protocol.comment(f'WASH {i+1}')
        mix_vol_wash = protocol.params.sample_vol + protocol.params.etoh80_vol
        #* changed bottom from 70 to 60 to ensure etoh pickup for all samples
        #* changed well.bottom() to well.bottom().move(Point(1,0,1)) to really get to the beads for mixing
        #* defaulted the dispense and mixing back to the middle of the well, it seemed to incorporate the beads better
        p300.transfer(protocol.params.etoh80_vol, etoh80.bottom(40), [well.bottom() for well in magwells]
                    , mix_after = (10, protocol.params.etoh80_vol if mix_vol_wash < 300 else 300, [well.bottom() for well in magwells])
                    , new_tip = 'always',
                    blow_out = True, blowout_location = 'destination well')
        
        magdeck.engage(height_from_base=5)
        protocol.delay(minutes=2, msg= 'Incubating on magnet for 2 minutes')

        #* need to split the aspiration into evens and odds again to account for bead position
        #! same switch to 'always' for new_tip here to avoid cross-contamination - same issue as above
        #! re-added the trash as the blowout location - think that is the standard, but better safe than sorry
        p300.flow_rate.aspirate = 25  # Slow down aspirate speed to avoid disturbing beads

        if odds != []:
            # odds
            p300.transfer(protocol.params.etoh80_vol * 1.1, [well.bottom().move(Point(-2,-2,1)) for well in odds], waste.top()
                            , new_tip = 'always', air_gap = 10,
                            blow_out = True, blowout_location = 'destination well')
        if evens != []:
            # evens
            p300.transfer(protocol.params.etoh80_vol * 1.1, [well.bottom().move(Point(2,-2,1)) for well in magwells], waste.top()
                            , new_tip = 'always', air_gap = 10,
                            blow_out = True, blowout_location = 'destination well')

    p300.flow_rate.aspirate = 94  # Reset to default aspirate speed
    magdeck.disengage()
    protocol.comment('Washing complete. Beads are now ready for digestion or elution.')
    