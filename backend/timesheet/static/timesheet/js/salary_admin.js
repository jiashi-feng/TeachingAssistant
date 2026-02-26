; (function () {
  function init() {
    const timesheetSelect = document.getElementById('id_timesheet')
    const amountInput = document.getElementById('id_amount')
    const detailsTextarea = document.getElementById('id_calculation_details')

    if (!timesheetSelect || !amountInput || !detailsTextarea) {
      return
    }

    const baseCalcUrl =
      (timesheetSelect.dataset && timesheetSelect.dataset.calcUrl) ||
      '/admin/timesheet/salary/calc-timesheet'

    async function fetchSalaryData(timesheetId) {
      if (!baseCalcUrl || !timesheetId) {
        amountInput.value = ''
        detailsTextarea.value = ''
        return
      }

      const sep = baseCalcUrl.endsWith('/') ? '' : '/'
      const url = `${baseCalcUrl}${sep}${timesheetId}/`

      try {
        const response = await fetch(url, {
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
          },
          credentials: 'include',
        })

        const data = await response.json()

        if (!response.ok) {
          const errorMsg = data.error || ''
          detailsTextarea.value = errorMsg
          amountInput.value = ''
          return
        }

        amountInput.value = data.amount || ''
        detailsTextarea.value = JSON.stringify(data.details, null, 2)
      } catch (error) {
        amountInput.value = ''
        detailsTextarea.value = '获取薪酬计算信息失败，请稍后重试。'
      }
    }

    let lastValue = ''

    function checkValueAndFetch() {
      const currentVal = timesheetSelect.value || ''
      let effectiveVal = currentVal

      // 结合 select2：如果有 jQuery，优先从 jQuery 视角读一次
      if (window.django && window.django.jQuery) {
        const $ = window.django.jQuery
        const v = $('#id_timesheet').val()
        if (Array.isArray(v) && v.length) {
          // 多选取最后一个
          if (v[v.length - 1]) {
            effectiveVal = v[v.length - 1]
          }
        } else if (typeof v === 'string' && v) {
          effectiveVal = v
        } else {
          effectiveVal = currentVal
        }
      } else {
        effectiveVal = currentVal
      }

      if (!effectiveVal || effectiveVal === '__placeholder__') {
        amountInput.value = ''
        detailsTextarea.value = ''
        lastValue = ''
        return
      }

      // 只有在值发生变化时才发请求，避免重复调用
      if (effectiveVal !== lastValue) {
        lastValue = effectiveVal
        fetchSalaryData(effectiveVal)
      }
    }

    // 轮询当前值变化，绕过 select2 的事件问题
    setInterval(checkValueAndFetch, 800)
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init)
  } else {
    init()
  }
})()
