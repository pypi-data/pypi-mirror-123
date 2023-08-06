#-z STRING true if string is empty
    #source FILENAME [arguments] used to read and execute contents of file
#[[ -z "${DB2CFG_PERSIST}" ]] && source /etc/profile
# we want source /mnt/blumeta0/db2_config/custom_registry.cfg ?

# variable "db2_regvar_file" holds the
# ${1:-} is something like ${parameter:-val} if the parameter is not being used then use the value as default
    # if $1 then db2_regvar_file = $1, else db2_regvar_file = $DB2CFG_PERSIST
#db2_regvar_file=${1:-${DB2CFG_PERSIST}/db2u-regvar.cfg}


#cat $db2_regvar_file | sed 's/^[ \t]*//;s/[ \t]*$//' | while IFS= read -r value; do
#    [[ $value =~ ^#|^$ ]] && continue , =~ regular expression match, continue used to skip the loop if expression match is true
#    echo db2set "$value" , else print 
#    ${HOME}/sqllib/adm/db2set "$value" 2>&1 , redirect standard error to 

#################### get parameters ########################

#################### Process custom_registry.cfg file #####################
# source /mnt/blumeta0/db2_config_custom_registry.cfg
# custom_registry_file=${1:-${...}/custom_registry.cfg}
# while IFS= read -r value; do                      # while read line; do echo $line; done < custom_registry.cfg ?
#   echo "db2set ${value}"
#   done
#################### Run custom_registry.cfg ####################
# 

# Get the custom_registry file to read and execute
source /mnt/blumeta0/db2_config/custom_registry.cfg
#
custom_registry_file=${1:-${...}/custom_registry.cfg}