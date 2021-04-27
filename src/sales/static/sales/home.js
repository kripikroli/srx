const reportBtn = document.getElementById('report-btn')

const chartImg = document.getElementById('chart-img')

const reportModal = document.getElementById('report-modal')
const reportModalBody = document.getElementById('report-modal-body')
const reportForm = document.getElementById('report-form')
const reportName = document.getElementById('id_name')
const reportRemarks = document.getElementById('id_remarks')
const reportSaveBtn = document.getElementById('report-modal-save-btn')
const alertBox = document.getElementById('alert-box')

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const closeModalBtn = document.getElementById('close-modal-btn')
const closeModalXBtn = document.getElementById('close-modal-x-btn')

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type}">
            ${msg}
        </div>
    `
}

if (chartImg) {
    reportBtn.classList.remove('is-hidden')
}

reportBtn.addEventListener('click', ()=> {
    reportModalBody.prepend(chartImg)
    reportModal.classList.add('is-active')

    reportSaveBtn.addEventListener('click', e => {
        e.preventDefault()

        const formData = new FormData()

        formData.append('csrfmiddlewaretoken', csrf)
        formData.append('name', reportName.value)
        formData.append('remarks', reportRemarks.value)
        formData.append('image', chartImg.src)

        $.ajax({
            type: 'POST',
            url: '/reports/save/',
            data: formData,
            success: function(response) {
                console.log(response)
                handleAlerts('success', 'Report was created')
            },
            error: function(error) {
                console.log(error)
                handleAlerts('danger', 'oppsss... something went wrong')
            },
            processData: false,
            contentType: false,
        })
    })
})

closeModalBtn.addEventListener('click', ()=> {
    reportModal.classList.remove('is-active')
})

closeModalXBtn.addEventListener('click', ()=> {
    reportModal.classList.remove('is-active')
})
