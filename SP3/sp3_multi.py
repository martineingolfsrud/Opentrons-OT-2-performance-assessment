# an attempt to incorporate the multi-channel pipette into the sp3 protocol. Figure out how to deal with the fact
# that I wish I had three pipette mounts (p20, p300, p300M) 
#! I am dealing with this through doing bead addition manually, as this is the only step where we need the p20,
#! and the robot takes ages and has to do it single channel, because loading beads into the reservoir would require
#! a stupid amount of beads, and they would probably just get stuck to the walls :)

from opentrons import protocol_api
from opentrons.types import Point
metadata = {
    'protocolName': 'SP3 Sample Preparation Multichannel v1.0',
    'description': '''This protocol performs SP3 sample preparation including protein binding and washing steps.''',
    'author': 'Martine'
}

requirements = {"robotType": "OT-2", "apiLevel": "2.24"} #2.27 is the latest api level as of january 2026, but the OT2 currently only supports 2.24 or older

def add_parameters(parameters: protocol_api.ParameterContext):
    # set parameters for the protocol (for now):
        # sample volume: we do 25 ul of sample s
        # bead volume: we do 2.5 ul of beads, to get a 10:1 (v/v) ratio with 25 ul sample 
        # etoh80 (washing) volume: this doesn't really matter anyway, so 180 ul will be enough 
    # chooseable parameters for the protocol:
    #? number of samples
    parameters.add_int(display_name = 'Number of Samples', variable_name='num_samples', default = 12, 
                        description='Number of samples to process. Max 96.', minimum = 8, maximum = 96) # the multichannel does 8 anyways

    #? number of replicates per sample
        # this might get removed and integrated into the number of samples instead to avoid confusion - it has no
        # real impact other than determining the number of wells needed
    parameters.add_int(display_name = 'Number of Replicates', variable_name='num_replicates', default = 1, 
                        description='Number of replicates per sample. Max 12.', minimum=1, maximum=12) # if only 8 samples, then 12 replicates fills the plate
    
    well_plate_rows = [
    {'display_name': 'A1', 'value': '0'}, {'display_name': 'A2', 'value': '8'}, {'display_name': 'A3', 'value': '16'},
    {'display_name': 'A4', 'value': '24'}, {'display_name': 'A5', 'value': '32'}, {'display_name': 'A6', 'value': '40'},
    {'display_name': 'A7', 'value': '48'}, {'display_name': 'A8', 'value': '56'}, {'display_name': 'A9', 'value': '64'},
    {'display_name': 'A10', 'value': '72'}, {'display_name': 'A11', 'value': '80'}, {'display_name': 'A12', 'value': '88'}]
    
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
    #? the starting well of a 96-well plate
    parameters.add_str(display_name = 'Starting Sample Column', variable_name = 'start_sample_well', default = '0', 
                        choices = well_plate)

    #? starting tip 300 ul pipette
    parameters.add_str(display_name = 'Starting Tip MC (6) 300 uL', variable_name = 'start_row_300', default = '0', 
                        choices = well_plate_rows)

    #? starting tip 20 ul pipette
    parameters.add_str(display_name = 'Starting Tip SC (9) 300 uL', variable_name = 'start_tip_300', default = '0', 
                        choices = well_plate)


def run(protocol: protocol_api.ProtocolContext):
    # beginning by creating secondary parameters based on the user input
    total_samples = int(protocol.params.num_samples) * int(protocol.params.num_replicates)

    # assume constant sample volume for now [ul]:
    #!!! we need to consider total volume in well (sample, beads, red/alc, water - we usually go for 52.5 ul?)
    sample_vol = 52.5
    etoh100_vol = (sample_vol/0.3) - sample_vol  # volume of 100% etoh needed to make 70% in the final volume
    etoh80_vol = 180  # volume of 80% etoh for washing step
    #bead_vol = 2.5  # volume of beads to add to each sample #! commenting this out, beads no longer needed

    # ------------- LABWARE SETUP -------------
    tips300 = protocol.load_labware('opentrons_96_tiprack_300ul', 9)
    tips300M = protocol.load_labware('opentrons_96_tiprack_300ul', 6) # for the multi-channel pipette, to avoid having to reuse tips for the etoh100 addition step
    reuse_300 = protocol.load_labware('opentrons_96_tiprack_300ul', 5) # for reuse of tips during ethanol washes
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tips300])
    p300M = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=[tips300M])
    p300.starting_tip = tips300.wells()[int(protocol.params.start_tip_300)]
    p300M.starting_tip = tips300M.wells()[int(protocol.params.start_row_300)]

    reservoir = protocol.load_labware('opentrons_tough_12_reservoir_22ml', 3) # for etoh and waste
    #eppendorfs = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 2) # for beads #! no need
    magdeck = protocol.load_module('magnetic module', 1)
    if magdeck.status == 'engaged':
        magdeck.disengage() # ensure it is off when beginning the protocol
    magplate = magdeck.load_labware('eppendorf_96_wellplate_500ul')

    # ------------- REAGENT SETUP -------------
    #beads = eppendorfs.wells_by_name()['A1'] # beads #! no need
    etoh100 = reservoir.wells_by_name()['A1'] # 100% EtOH
    etoh80 = reservoir.wells_by_name()['A2'] # 80% EtOH
    waste = reservoir.wells_by_name()['A12'] # waste container for supernatant

    mix_vol = (sample_vol + etoh100_vol)*0.9 # for addition of etoh100 
    mix_vol_wash = sample_vol + 180 # for washing with etoh80
    # ------------- SAMPLE WELLS SETUP -------------
    start_well_index = int(protocol.params.start_sample_well) #where to start using .wells() indexing
    magwells = magplate.wells()[start_well_index : start_well_index + int(total_samples)] #this is a list object, containing all wells to be filled during the protocol

    available_wells = 96 - start_well_index 
    if total_samples > available_wells:
        protocol.pause(f"Not enough wells in the plate starting from {protocol.params.start_sample_well}. Please use a new plate or adjust the number of samples/replicates.")
        raise Exception("Not enough wells in the plate.")

    # -------------- SPLIT INTO EVENS AND ODDS --------------
        # this is in order to account for every other column pushing the beads to different sides of the well
        # assuring aspiration does not disturb the beads independently of whether they are to the left or right
        # side of the well
    
        # I need two lists that work for the multi-channel pipette, splitting only row A into evens and odds, and I also need
        # two lists that work for the single-channel pipette, splitting all wells into evens and odds
        # I solve this by splitting all wells into evens and odds, and then creating multi-channel specific lists after
    evens = []
    odds = []

    for well in magwells:
        # Extract the column number from the well name
        column_number = int(well.well_name[1:])  # Extract the numeric part of the well name
        if column_number % 2 == 0:  # Check if the column number is even
            evens.append(well)
        else:
            odds.append(well)

    evens_300 = [well for well in evens if well.well_name[0] == 'A'] # for the multi-channel pipette, we only care about row A
    odds_300 = [well for well in odds if well.well_name[0] == 'A'] # for the multi-channel pipette, we only care about row A

    # Debugging: Print the results
    protocol.comment(f"Evens: {[well.well_name for well in evens]}")
    protocol.comment(f"Odds: {[well.well_name for well in odds]}")
    protocol.comment(f"Evens for multi-channel: {[well.well_name for well in evens_300]}")
    protocol.comment(f"Odds for multi-channel: {[well.well_name for well in odds_300]}")

    # ------------- FUNCTIONS -------------
    '''
    def add_beads(well):
        # 1: adding the beads
        p20.transfer(bead_vol, beads, well, new_tip = 'always', blow_out = True, blowout_location = 'destination well')
    '''
    # 2: adding etoh to final conc. of 70%
    def add_etoh100(well):
        #! this is now done by the multichannel pipette, so 'well' needs to refer to wells in row A only
        p300M.transfer(etoh100_vol, etoh100, well
                , mix_after = (10, mix_vol if mix_vol < 300 else 300, well.bottom(1))
                , new_tip = 'always', blow_out = True, blowout_location = 'destination well') 
    '''
    def bead_agg():
        # just mixing the beads in the eppendorf tube so they dont stick
        p20.pick_up_tip()
        p20.mix(10, 20, beads.bottom(1))
        p20.blow_out(beads.bottom(1))
        p20.drop_tip()
    '''
    def wash_func(odds, well, i):
        # red because of my notes; does the steps for all wells in the list 
        #movePoint = Point(-1,0,1) if odds else Point(1,0,1) # this is the point we will move to for the odd and even wells respectively, to account for bead position
        # 1: removing supernatant
        #! this transfer command has been rewritten like below (#2) in order to reuse tips for each wash
        p300M.flow_rate.aspirate = 25
        p300M.pick_up_tip(reuse_300.wells()[i+1]) # pick up the first tip for reuse during washes
        p300M.aspirate(etoh80_vol*1.1, well.bottom()) 
        p300M.dispense(location=waste.top())
        p300M.blow_out(waste.top())
        p300M.drop_tip(reuse_300.wells()[i+1]) # drop the tip back
        #2: adding etoh80
        p300M.flow_rate.aspirate = 94  # reset to default aspirate speed for the wash step
        p300M.pick_up_tip(location=reuse_300.wells()[0])
        p300M.aspirate(etoh80_vol, etoh80)
        p300M.dispense(location=well.top())
        p300M.blow_out(well.top())
        p300M.drop_tip(location=reuse_300.wells()[0]) 

    def mix_func(wells):
        # mixes after ALL wells have been washed
        for well in wells:
            p300M.pick_up_tip()
            p300M.mix(10, etoh80_vol if mix_vol_wash < 300 else 300, well.bottom())
            p300M.blow_out(well.bottom())
            p300M.drop_tip()




    # ------------- PROTOCOL STEPS -------------
    protocol.comment('Starting the SP3 protocol!')
    protocol.comment(f'Total samples including replicates: {total_samples}')
    protocol.comment(f'Using wells: {[well.well_name for well in magwells]}')

    # STEP 1: add beads to each sample and STEP 2: add 100% EtOH to each sample for a final concentration of 70%
            # STEP 1 bug fixes:
            #* no need to have mixing here, the small volume doesn't allow for it anyway
            #* added blowout - it seems like some sample doesn't come out otherwise and ends up in the trash
            # STEP 2 bug fixes:
            #* changed bottom from 70 to 60, to ensure etoh pickup for all samples - and then to 40?
            #* changed mix_vol - it currently picks up MORE than there is in the well, but multiplying by 0.9 should resolve this
            #* added blowout! turns out the beads can clog the pipette and then two bad things happen - 1: mixing does not occur
            #* 2: it slowly picks up volume, but then dispenses all of it in the trash, because it assumes it is empty 
    '''
    protocol.comment('Step 1: Adding beads to each sample and Step 2: Adding 100% EtOH to each sample for a final concentration of 70%')

    if odds!= [] and len(evens)>=8: # if there are odd wells to process
        for well in odds[:int(len(odds)/2)]: # first half of odd wells then agg
            add_beads(well)
        
        bead_agg() 

        for well in odds[int(len(odds)/2):]: # second half of odd wells then agg
            add_beads(well)
        
        bead_agg() 
    
    elif odds!= [] and len(odds)<8: # if there are odd wells to process but less than 6, we can just do them all at once without the need for an additional agg step
        for well in odds:
            add_beads(well)
    
    if evens != [] and len(evens)>=8: # if there are even wells to process
        for well in evens[:int(len(evens)/2)]: # first half of even wells then agg
            add_beads(well)
        bead_agg() 
        
        for well in evens[int(len(evens)/2):]: # second half of even wells then agg
            add_beads(well)
        
        bead_agg()

    elif evens != [] and len(evens)<8: # if there are even wells to process but less than 6, we can just do them all at once without the need for an additional agg step
        for well in evens:
            add_beads(well)
    '''
    protocol.comment('Step 1: Adding EtOH100 to each sample for a final concentration of 70%')
    # NOW add etoh100 to all wells, using the multi-channel pipette #! this is a new step, should work but needs testing
    for well in odds_300:
        add_etoh100(well)
    
    for well in evens_300:
        add_etoh100(well)
    
    # STEP 3 Incubate at 24°C for 7 minutes manually
    protocol.pause('Step 3: Incubate samples at 24°C for 7 minutes. Click RESUME when done.')
    protocol.comment('Resuming protocol')

    # STEP 4: Engage magnetic module and wait for beads to collect
    protocol.comment('Step 4: Engaging magnetic module and waiting for beads to collect')
    magdeck.engage(height_from_base=5)
    #protocol.delay(minutes=5, msg= 'Incubating on magnet for 5 minutes') # wait 5 minutes
    protocol.comment('Beads should now be collected on the magnet.')

    # STEP 5: Remove supernatant after initial incubation AND STEP 6: Washing with 80% EtOH
        # these steps need to be combined in order to avoid beads drying out too much
            # STEP 5 bug fixes:
            #* moving the aspiration here to the sides - aka splitting into two commands (odds and evens)
            #* the blowout_location was source well, but if there is leftover supernatant i'd want it do be blown out into waste (destination well)
            #* changed new_tip to 'always' to avoid cross-contamination when removing supernatant - it was 'once' before, which worked fine,
            #* but splitting into evens and odds seems to have done something to it - better safe than sorry
            # STEP 6 bug fixes:
            #* changed bottom from 70 to 60 to ensure etoh pickup for all samples (and then to 40?)
            #* changed well.bottom() to well.bottom().move(Point(1,0,1)) to really get to the beads for mixing - later removed this again, as it seemed to make mixing worse
            #* defaulted the dispense and mixing back to the middle of the well, it seemed to incorporate the beads better
            #* need to split the aspiration into evens and odds again to account for bead position
            #* same switch to 'always' for new_tip here to avoid cross-contamination - same issue as above
            #* re-added the trash as the blowout location - think that is the standard, but better safe than sorry

    protocol.comment('Step 5: Removing supernatant and Step 6: Washing with 80% EtOH')
    
    for i in range(3): # we do 3 washes with etoh80
        # REMOVING SN AND ADDING ETOH80 FOR WASH 1 and 2 PLUS ADDING ETOH80 FOR WASH 3
        
        if odds_300!= []: # if there are odd wells to process
            for j, well in enumerate(odds_300):
                wash_func(odds = True, well = well, i=j+7)
        
        if evens_300 != []: # if there are even wells to process
            for j, well in enumerate(evens_300):
                wash_func(odds = False, well= well, i=j+15)
        
        magdeck.disengage() # need to disengage to mix the samples
        mix_func(evens_300) # mixing after all wells have been washed
        mix_func(odds_300) # mixing after all wells have been washed
        magdeck.engage(height_from_base=5) # re-engage to let the beads collect again before the next wash
        protocol.delay(minutes=2, msg= 'Incubating on magnet for 2 minutes')

    # REMOVING SN FROM WASH 3 - this is the last step !!!! 
    p300.flow_rate.aspirate = 25
    
    if odds_300!= []: # if there are odd wells to process
        for well in odds_300:
            p300.transfer(etoh80_vol * 1.1, well.bottom().move(Point(-1,0,1)), waste.top(), new_tip = 'always', air_gap = 10,
                blow_out = True, blowout_location = 'destination well')

    if evens_300 != []: # if there are even wells to process
        for well in evens_300:
            p300.transfer(etoh80_vol * 1.1, well.bottom().move(Point(1,0,1)), waste.top(), new_tip = 'always', air_gap = 10,
                blow_out = True, blowout_location = 'destination well')


    p300.flow_rate.aspirate = 94  # Reset to default aspirate speed
    magdeck.disengage()
    protocol.comment('Washing complete. Beads are now ready for digestion.')
    


