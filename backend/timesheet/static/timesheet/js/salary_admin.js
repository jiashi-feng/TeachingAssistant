document.addEventListener('DOMContentLoaded', function () {
  const timesheetSelect = document.getElementById('id_timesheet')
  const amountInput = document.getElementById('id_amount')
  const detailsTextarea = document.getElementById('id_calculation_details')

  if (!timesheetSelect || !amountInput || !detailsTextarea) {
    return
  }

  const baseCalcUrl =
    (timesheetSelect.dataset && timesheetSelect.dataset.calcUrl) ||
    '/admin/timesheet/salary/calc-timesheet'

  let lastSelectedId = ''

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
        return
      }

      amountInput.value = data.amount || ''
      detailsTextarea.value = JSON.stringify(data.details, null, 2)
    } catch (error) {
      amountInput.value = ''
      detailsTextarea.value = '获取薪酬计算信息失败，请稍后重试。'
    }
  }

  function resolveSelectedId(event) {
    let selectedId = ''

    const readFromDom = () => {
      // 1. 直接读取 select 的 selectedIndex
      if (typeof timesheetSelect.selectedIndex === 'number' && timesheetSelect.selectedIndex >= 0) {
        const option = timesheetSelect.options[timesheetSelect.selectedIndex]
        if (option) {
          const val = option.getAttribute('value') ?? option.value
          if (val !== undefined && val !== null && val !== '') {
            return val
          }
        }
      }

      // 2. 原生 value
      if (timesheetSelect.value) {
        return timesheetSelect.value
      }

      // 3. selectedOptions
      if (timesheetSelect.selectedOptions && timesheetSelect.selectedOptions.length) {
        const option = timesheetSelect.selectedOptions[timesheetSelect.selectedOptions.length - 1]
        if (option) {
          return option.getAttribute('value') ?? option.value ?? ''
        }
      }

      // 4. jQuery / select2 值
      if (window.django && window.django.jQuery) {
        const val = window.django.jQuery(timesheetSelect).val()
        if (Array.isArray(val) && val.length) {
          return val[val.length - 1]
        }
        if (typeof val === 'string') {
          return val
        }
      }

      // 5. data-selected-id
      if (timesheetSelect.dataset && timesheetSelect.dataset.selectedId) {
        return timesheetSelect.dataset.selectedId
      }

      return ''
    }

    // 1. 直接读取 select 值
    selectedId = readFromDom()

    // 2. select2 事件参数
    if ((!selectedId || selectedId === '') && event && event.params && event.params.data) {
      selectedId =
        event.params.data.id ??
        event.params.data.value ??
        selectedId
    }

    // 3. 再次从 DOM 读取，确保 select2 已写入值
    if (!selectedId || selectedId === '') {
      selectedId = readFromDom()
    }

    // 去除空字符串及 placeholder
    if (selectedId === null || selectedId === undefined || selectedId === '') {
      return ''
    }

    return selectedId.toString()
  }

  function bindEvents() {
    console.log('[salary_admin] binding events')

    const scheduleFetch = (event) => {
      setTimeout(() => {
        const selectedId = resolveSelectedId(event)
        if (selectedId && selectedId !== lastSelectedId) {
          lastSelectedId = selectedId
          fetchSalaryData(selectedId)
        }
      }, 150)
    }

    // 原生 change 事件
    timesheetSelect.addEventListener('change', scheduleFetch, true)

    document.addEventListener(
      'change',
      (event) => {
        if (event.target === timesheetSelect) {
          scheduleFetch(event)
        }
      },
      true
    )

    // 兼容 Django Admin 的 select2
    if (window.django && window.django.jQuery) {
      const $ = window.django.jQuery
      $(document).on('select2:select change.select2 select2:close', '#id_timesheet', (event) => {
        scheduleFetch(event)
      })
    }
  }

  // 强制只读（即使浏览器未渲染readonly属性）
  amountInput.readOnly = true
  detailsTextarea.readOnly = true

  bindEvents()

  // 编辑页面刷新后自动加载
  const initialVal = resolveSelectedId()
  if (initialVal) {
    lastSelectedId = initialVal
    console.log('[salary_admin] initial value detected, fetching…', initialVal)
    fetchSalaryData(initialVal, 'initial')
  }

  // 兜底轮询：兼容未触发事件的场景（如弹窗选择）
  setInterval(() => {
    const current = resolveSelectedId()
    if (current && current !== lastSelectedId) {
      console.log('[salary_admin] poll detected change:', current)
      lastSelectedId = current
      fetchSalaryData(current, 'poll')
    }
  }, 1000)
})

