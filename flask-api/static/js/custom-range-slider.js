// https://nikitahl.com/style-range-input-css

const rangeInputs = document.querySelectorAll('input[type="range"]')
const numberInput = document.querySelector('input[type="number"]')

function handleInputChange(e) {
  let target = e.target
  if (e.target.type !== 'range') {
    target = document.getElementById('range')
  } 
  const min = target.min
  const max = target.max
  const val = target.value

  const maxWidth = target.parentElement.offsetWidth
  const btnWidth = target.parentElement.getElementsByTagName('input')[1].offsetWidth
  const percent = (val - min) * 100 / (max - min)

  target.style.backgroundSize = percent+'% 100%'
  var left_position = (percent/9.85) * btnWidth

  target.parentElement.getElementsByTagName('input')[1].style.left = left_position+'px'
}

rangeInputs.forEach(input => {
  input.addEventListener('input', handleInputChange)
})

numberInput.addEventListener('input', handleInputChange)
