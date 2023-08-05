function submit_data() {
    let documents = document.forms['markdown-form'].elements
    let data = {}

    for (let [key, element] of Object.entries(documents)) {
        // Use element name as key if specified
        key = element.name ? element.name : key
        
        // Set the checked state of a checkbox
        if (element.type && element.type == 'checkbox') {
            data[key] = element.checked
        }

        // Set the value of a radio button if it is checked
        else if (element.type && element.type == 'radio') {
            if (element.checked == true) {
                data[key] = element.value
            }
            else if (!(key in data)) {
                data[key] = undefined
            }
        }

        // Return the value for everything else
        else {
            data[key] = element.value
        }
    }

    pywebview.api.submit_data(data)
}