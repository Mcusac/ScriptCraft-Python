@echo off
:: ScriptCraft Configuration (Auto-Generated)
:: Generated from config.yaml for tool: rhq_form_autofiller
:: Last updated: Fri 08/22/2025  9:55:37.73

set "TOOL_TO_SHIP=rhq_form_autofiller"
set "TOOL_DESCRIPTION=🏠 Automatically fills RHQ residential history forms using participant data"
set "ENTRY_COMMAND=-m scriptcraft.tools.rhq_form_autofiller.main"
set "COMMON_PACKAGES=setuptools wheel pandas numpy openpyxl python-docx pyyaml pytz python-dateutil selenium"
set "TOOL_PACKAGES=pyyaml pandas python-docx openpyxl selenium pytz"
set "URL_TEMPLATE=https://iappsecqa.hosts.hsc.unt.edu/itredc/residential-history/{med_id}"

echo SUCCESS: Configuration loaded successfully
echo Tool to ship: %TOOL_TO_SHIP%
echo Description: %TOOL_DESCRIPTION%
echo Entry command: %ENTRY_COMMAND%
echo Common packages: %COMMON_PACKAGES%
echo Tool packages: %TOOL_PACKAGES%
echo URL template: %URL_TEMPLATE%
