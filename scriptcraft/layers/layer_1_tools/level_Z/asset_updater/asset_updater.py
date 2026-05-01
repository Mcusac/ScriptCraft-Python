# utilize user_changed.csv and location_changed.csv to update the asset updater page
    # load and combine both. be sure to drop duplicates on the column "Tag Number"
    # from user_changed.csv: columns "Tag Number", "user_norm_forms"
        # some values in Tag Number column may be lacking their three leading zeros, so we need to add them (ie 47072 -> 00047072)
        # need to get the employee id in the user_changed.csv column "user_norm_forms"
    # from location_changed.csv: columns "Tag Number", "location_norm_forms"
        # need to update location_norm_forms to be the exact string required for input into the asset updater page
        # same tag number issue as above (ie 47072 -> 00047072)

# open browser and navigate to the asset updater page
    # may need to login first and use duomobile for first login of day

# select Business Unit entry
    # <input type="text" name="GBAM_SRCH_VW_BUSINESS_UNIT" id="GBAM_SRCH_VW_BUSINESS_UNIT" aria-describedby="PTS_CRITTEXT_DISP GBAM_SRCH_VW_BUSINESS_UNIT_LBL GBAM_SRCH_VW_BUSINESS_UNIT$OP  NONEFOUND" onkeydown="javascript:doKeyEnter(event,'PTS_CFG_CL_WRK_PTS_SRCH_BTN')" onkeypress="javascript:cancelBubble(event);" tabindex="67" value="" class="PSEDITBOX" style="width:140px; " maxlength="5" aria-required="true">

# enter in the value "HS763"

# select Tag number entry
    # <input type="text" name="GBAM_SRCH_VW_TAG_NUMBER" id="GBAM_SRCH_VW_TAG_NUMBER" aria-describedby="GBAM_SRCH_VW_TAG_NUMBER_LBL GBAM_SRCH_VW_TAG_NUMBER$OP  NONEFOUND" onkeydown="javascript:doKeyEnter(event,'PTS_CFG_CL_WRK_PTS_SRCH_BTN')" onkeypress="javascript:cancelBubble(event);" tabindex="74" value="" class="PSEDITBOX" style="width:140px; " maxlength="12">

# enter in the value for tag number


# wait for the page to load

# click into Date of Transfer entry 
    # <input type="text" name="GBAM_ASSET_REQ_DATE_TRANSFER$0" id="GBAM_ASSET_REQ_DATE_TRANSFER$0" tabindex="21" value="04/30/2026" class="PSEDITBOX" style="width:71px; " maxlength="10" onkeyup="if (isPromptKey(event))DatePrompt_win0('GBAM_ASSET_REQ_DATE_TRANSFER$0','GBAM_ASSET_REQ_DATE_TRANSFER$0','450',false);return false;">

# enter in current date using the format MM/DD/YYYY

# click on location spyglass button
    # <img src="/cs/ps/cache_86117/PT_PROMPT_LOOKUP_1.gif" title="Look up Location" alt="Look up Location" id="LOCATION_VW_DESCR$prompt$img$0" border="0" align="absmiddle" style="vertical-align:middle;">

# wait for modal to appear

# click on Location code entry
    # <input type="text" name="LOCATION_VW_LOCATION" id="LOCATION_VW_LOCATION" aria-describedby="LOCATION_VW_LOCATION_LBL LOCATION_VW_LOCATION$OP  NONEFOUND" tabindex="16" value="" class="PSEDITBOX" style="width:140px; " maxlength="10">

# enter in fixed value corresonding to the chosen tag number from location_changed.csv in the column "location_norm_forms"

# hit enter or click "Look Up" button to search
    # <input type="button" id="#ICSearch" name="#ICSearch" class="PSPUSHBUTTONTBLOOKUP" value="Look Up" onclick="javascript:submitAction_win0(document.win0, '#ICSearch');" tabindex="21" psaccesskey="\">

# wait for the page to load

# click on search result table under location code column that matches the searched location code
    # <a id="SEARCH_RESULT1" name="RESULT1$0" aria-describedby="app_label PSSRCHSUBTITLE PSSRCHINSTRUCTIONS" class="PSSRCHRESULTSODDROW" href="javascript:doUpdateParent(document.win0,'#ICRow0');">PCC  6S1</a>
    # this will have 1 less space between the first and second part of the location code

# wait for page to load and modal to close

# click on Custodian spyglass button
    # <img src="/cs/ps/cache_86117/PT_PROMPT_LOOKUP_1.gif" title="Look up Custodian" alt="Look up Custodian" id="PERSONAL_DATA_NAME$prompt$img$0" border="0" align="absmiddle" style="vertical-align:middle;">

# wait for modal to appear

# click on Employee ID entry
    # <input type="button" id="#ICSearch" name="#ICSearch" class="PSPUSHBUTTONTBLOOKUP" value="Look Up" onclick="javascript:submitAction_win0(document.win0, '#ICSearch');" tabindex="21" psaccesskey="\">

# enter in the value for employee id

# hit enter or click "Look Up" button to search
    # <input type="button" id="#ICSearch" name="#ICSearch" class="PSPUSHBUTTONTBLOOKUP" value="Look Up" onclick="javascript:submitAction_win0(document.win0, '#ICSearch');" tabindex="21" psaccesskey="\">

# wait for the page to load

# click on search result table under Employee ID column that matches the searched employee id
    # <a id="SEARCH_RESULT1" name="RESULT0$0" aria-describedby="app_label PSSRCHSUBTITLE PSSRCHINSTRUCTIONS" class="PSSRCHRESULTSODDROW" href="javascript:doUpdateParent(document.win0,'#ICRow0');">	 10989693</a>

# wait for page to load and modal to close

# click on Update this Asset button
    # <input type="button" name="AM_MY_ASSET_WRK_SUBMIT_PB" id="AM_MY_ASSET_WRK_SUBMIT_PB" tabindex="32" value="Update this Asset" class="PSPUSHBUTTON" style="width:132px; " onclick="submitAction_win0(document.win0,this.id,event);" title="Submit PB">


# Wait for page to load and a message modal to appear

# click ok button
    # <input type="button" id="#ICOK" name="#ICOK" class="PSPUSHBUTTONTBOK" value="OK" onclick="closeMsg(this);" tabindex="1">

# wait for page to load and modal to close

# click on return to search button
    # <input type="button" id="#ICList" name="#ICList" class="PSPUSHBUTTONTBRETURN PSPUSHBUTTONTBRETURNA" value="Return to Search" onclick="if (saveWarning('',document.win0,'_self', 'javascript:submitAction_win0(document.win0, \'#ICList\')')) javascript:submitAction_win0(document.win0, '#ICList');" tabindex="5000" psaccesskey="\">


# wait for page to load

# The business unit entry does not need to be entered again, it should stay on HS763

# The asset Identification number entry will now be filled but needs to be blanked out
    # <input type="text" name="GBAM_SRCH_VW_ASSET_ID" id="GBAM_SRCH_VW_ASSET_ID" aria-describedby="GBAM_SRCH_VW_ASSET_ID_LBL GBAM_SRCH_VW_ASSET_ID$OP  NONEFOUND" onkeydown="javascript:doKeyEnter(event,'PTS_CFG_CL_WRK_PTS_SRCH_BTN')" onkeypress="javascript:cancelBubble(event);" tabindex="71" value="000001016694" class="PSEDITBOX" style="width:140px; " maxlength="12">

# click on the Tag number entry
    # <input type="text" name="GBAM_SRCH_VW_ASSET_ID" id="GBAM_SRCH_VW_ASSET_ID" aria-describedby="GBAM_SRCH_VW_ASSET_ID_LBL GBAM_SRCH_VW_ASSET_ID$OP  NONEFOUND" onkeydown="javascript:doKeyEnter(event,'PTS_CFG_CL_WRK_PTS_SRCH_BTN')" onkeypress="javascript:cancelBubble(event);" tabindex="71" value="000001016694" class="PSEDITBOX" style="width:140px; " maxlength="12">

# click search button
    # <input type="button" name="PTS_CFG_CL_WRK_PTS_SRCH_BTN" id="PTS_CFG_CL_WRK_PTS_SRCH_BTN" tabindex="127" value="Search" class="PSPUSHBUTTON" style="width:89px; " onclick="submitAction_win0(document.win0,this.id,event);" accesskey="1">

# continue loop until all rows are updated