Object.defineProperty(exports, "__esModule", { value: true });
exports.Slider = void 0;
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
function RangeSlider(_a) {
    var _b;
    var { value, allowedValues, showCustomInput, name, disabled, placeholder, formatLabel, className, onBlur, onChange, forwardRef, showLabel = true } = _a, props = (0, tslib_1.__rest)(_a, ["value", "allowedValues", "showCustomInput", "name", "disabled", "placeholder", "formatLabel", "className", "onBlur", "onChange", "forwardRef", "showLabel"]);
    const [sliderValue, setSliderValue] = (0, react_1.useState)(allowedValues ? allowedValues.indexOf(Number(value || 0)) : value);
    (0, react_1.useEffect)(() => {
        updateSliderValue();
    }, [value]);
    function updateSliderValue() {
        var _a;
        if (!(0, utils_1.defined)(value)) {
            return;
        }
        const newSliderValueIndex = (_a = allowedValues === null || allowedValues === void 0 ? void 0 : allowedValues.indexOf(Number(value || 0))) !== null && _a !== void 0 ? _a : -1;
        // If `allowedValues` is defined, then `sliderValue` represents index to `allowedValues`
        if (newSliderValueIndex > -1) {
            setSliderValue(newSliderValueIndex);
            return;
        }
        setSliderValue(value);
    }
    function getActualValue(newSliderValue) {
        if (!allowedValues) {
            return newSliderValue;
        }
        // If `allowedValues` is defined, then `sliderValue` represents index to `allowedValues`
        return allowedValues[newSliderValue];
    }
    function handleInput(e) {
        const newSliderValue = parseInt(e.target.value, 10);
        setSliderValue(newSliderValue);
        onChange === null || onChange === void 0 ? void 0 : onChange(getActualValue(newSliderValue), e);
    }
    function handleCustomInputChange(e) {
        setSliderValue(parseInt(e.target.value, 10) || 0);
    }
    function handleBlur(e) {
        if (typeof onBlur !== 'function') {
            return;
        }
        onBlur(e);
    }
    function getSliderData() {
        if (!allowedValues) {
            const { min, max, step } = props;
            return {
                min,
                max,
                step,
                actualValue: sliderValue,
                displayValue: sliderValue,
            };
        }
        const actualValue = allowedValues[sliderValue];
        return {
            step: 1,
            min: 0,
            max: allowedValues.length - 1,
            actualValue,
            displayValue: (0, utils_1.defined)(actualValue) ? actualValue : (0, locale_1.t)('Invalid value'),
        };
    }
    const { min, max, step, actualValue, displayValue } = getSliderData();
    return (<div className={className} ref={forwardRef}>
      {!showCustomInput && showLabel && (<Label htmlFor={name}>{(_b = formatLabel === null || formatLabel === void 0 ? void 0 : formatLabel(actualValue)) !== null && _b !== void 0 ? _b : displayValue}</Label>)}
      <SliderAndInputWrapper showCustomInput={showCustomInput}>
        <exports.Slider type="range" name={name} min={min} max={max} step={step} disabled={disabled} onInput={handleInput} onMouseUp={handleBlur} onKeyUp={handleBlur} value={sliderValue} hasLabel={!showCustomInput}/>
        {showCustomInput && (<input_1.default placeholder={placeholder} value={sliderValue} onChange={handleCustomInputChange} onBlur={handleInput}/>)}
      </SliderAndInputWrapper>
    </div>);
}
const RangeSliderContainer = react_1.default.forwardRef(function RangeSliderContainer(props, ref) {
    return <RangeSlider {...props} forwardRef={ref}/>;
});
exports.default = RangeSliderContainer;
exports.Slider = (0, styled_1.default)('input') `
  /* stylelint-disable-next-line property-no-vendor-prefix */
  -webkit-appearance: none;
  width: 100%;
  background: transparent;
  margin: ${p => p.theme.grid}px 0 ${p => p.theme.grid * (p.hasLabel ? 2 : 1)}px;

  &::-webkit-slider-runnable-track {
    width: 100%;
    height: 3px;
    cursor: pointer;
    background: ${p => p.theme.border};
    border-radius: 3px;
    border: 0;
  }

  &::-moz-range-track {
    width: 100%;
    height: 3px;
    cursor: pointer;
    background: ${p => p.theme.border};
    border-radius: 3px;
    border: 0;
  }

  &::-ms-track {
    width: 100%;
    height: 3px;
    cursor: pointer;
    background: ${p => p.theme.border};
    border-radius: 3px;
    border: 0;
  }

  &::-webkit-slider-thumb {
    box-shadow: 0 0 0 3px ${p => p.theme.background};
    height: 17px;
    width: 17px;
    border-radius: 50%;
    background: ${p => p.theme.active};
    cursor: pointer;
    /* stylelint-disable-next-line property-no-vendor-prefix */
    -webkit-appearance: none;
    margin-top: -7px;
    border: 0;
  }

  &::-moz-range-thumb {
    box-shadow: 0 0 0 3px ${p => p.theme.background};
    height: 17px;
    width: 17px;
    border-radius: 50%;
    background: ${p => p.theme.active};
    cursor: pointer;
    /* stylelint-disable-next-line property-no-vendor-prefix */
    -webkit-appearance: none;
    margin-top: -7px;
    border: 0;
  }

  &::-ms-thumb {
    box-shadow: 0 0 0 3px ${p => p.theme.background};
    height: 17px;
    width: 17px;
    border-radius: 50%;
    background: ${p => p.theme.active};
    cursor: pointer;
    /* stylelint-disable-next-line property-no-vendor-prefix */
    -webkit-appearance: none;
    margin-top: -7px;
    border: 0;
  }

  &::-ms-fill-lower {
    background: ${p => p.theme.border};
    border: 0;
    border-radius: 50%;
  }

  &::-ms-fill-upper {
    background: ${p => p.theme.border};
    border: 0;
    border-radius: 50%;
  }

  &:focus {
    outline: none;

    &::-webkit-slider-runnable-track {
      background: ${p => p.theme.border};
    }

    &::-ms-fill-upper {
      background: ${p => p.theme.border};
    }

    &::-ms-fill-lower {
      background: ${p => p.theme.border};
    }
  }

  &[disabled] {
    &::-webkit-slider-thumb {
      background: ${p => p.theme.border};
      cursor: default;
    }

    &::-moz-range-thumb {
      background: ${p => p.theme.border};
      cursor: default;
    }

    &::-ms-thumb {
      background: ${p => p.theme.border};
      cursor: default;
    }

    &::-webkit-slider-runnable-track {
      cursor: default;
    }

    &::-moz-range-track {
      cursor: default;
    }

    &::-ms-track {
      cursor: default;
    }
  }
`;
const Label = (0, styled_1.default)('label') `
  font-size: 14px;
  margin-bottom: ${p => p.theme.grid}px;
  color: ${p => p.theme.subText};
`;
const SliderAndInputWrapper = (0, styled_1.default)('div') `
  display: grid;
  align-items: center;
  grid-auto-flow: column;
  grid-template-columns: 4fr ${p => p.showCustomInput && '1fr'};
  grid-gap: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=rangeSlider.jsx.map