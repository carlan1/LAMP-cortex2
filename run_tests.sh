green=`tput setaf 2`
cyan=`tput setaf 6`
reset=`tput sgr0`
find tests -name '*tests.py' -print0 |
    while IFS= read -r -d '' line; do
        echo "${line}"
        if [[ $line = "tests/primary_feature_tests.py" ]]
        then
            echo "${green} Running tests for ${line} ${reset}"
            coverage run "$line"
            echo "${cyan} Coverage Report for ${line}"
            coverage report -m cortex/primary/significant_locations.py
            coverage report -m cortex/primary/trips.py
            coverage report -m cortex/primary/screen_active.py
        else
            echo "TODO: add other tests here"
            # coverage report
        fi
    done
echo "${reset}"
 