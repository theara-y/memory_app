$('table').on('click', function(event) {
    const target = $(event.target)
    if (target.hasClass('show-ans-btn')) {
        target.addClass('hidden-group')
        target.next().removeClass('hidden-group')
    }

    if (target.hasClass('perfect-recall-btn') ||
        target.hasClass('partial-recall-btn') ||
        target.hasClass('failed-recall-btn')) {

        let id = target.closest('[data-id]').data('id')
        let outcome = target.data('outcome')

        submitOutcome(id, outcome, target)
    }
})

function submitOutcome(id, outcome, target) {
    let json = {
        "memory_id": id,
        "recall_outcome": outcome
    }

    axios.patch('report_recall_outcome', json)
        .then(res => {
            target.closest('.report-outcome-btns').html(target.html())
        })
}