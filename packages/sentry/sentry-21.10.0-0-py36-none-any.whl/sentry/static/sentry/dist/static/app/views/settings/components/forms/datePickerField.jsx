Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const dropdownMenu_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownMenu"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const icons_1 = require("app/icons");
const input_1 = require("app/styles/input");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const inputField_1 = (0, tslib_1.__importDefault)(require("./inputField"));
function handleChangeDate(onChange, onBlur, date, close) {
    onChange(date);
    onBlur(date);
    // close dropdown menu
    close();
}
const Calendar = (0, react_1.lazy)(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('./calendarField'))));
function DatePickerField(props) {
    return (<inputField_1.default {...props} field={({ onChange, onBlur, value, id }) => {
            const dateObj = new Date(value);
            const inputValue = !isNaN(dateObj.getTime()) ? dateObj : new Date();
            const dateString = (0, moment_1.default)(inputValue).format('LL');
            return (<dropdownMenu_1.default keepMenuOpen>
            {({ isOpen, getRootProps, getActorProps, getMenuProps, actions }) => (<div {...getRootProps()}>
                <InputWrapper id={id} {...getActorProps()} isOpen={isOpen}>
                  <StyledInput readOnly value={dateString}/>
                  <CalendarIcon>
                    <icons_1.IconCalendar />
                  </CalendarIcon>
                </InputWrapper>

                {isOpen && (<CalendarMenu {...getMenuProps()}>
                    <react_1.Suspense fallback={<placeholder_1.default width="332px" height="282px">
                          <loadingIndicator_1.default />
                        </placeholder_1.default>}>
                      <Calendar date={inputValue} onChange={date => handleChangeDate(onChange, onBlur, date, actions.close)}/>
                    </react_1.Suspense>
                  </CalendarMenu>)}
              </div>)}
          </dropdownMenu_1.default>);
        }}/>);
}
exports.default = DatePickerField;
const InputWrapper = (0, styled_1.default)('div') `
  ${input_1.inputStyles}
  cursor: text;
  display: flex;
  z-index: ${p => p.theme.zIndex.dropdownAutocomplete.actor};
  ${p => p.isOpen && 'border-bottom-left-radius: 0'}
`;
const StyledInput = (0, styled_1.default)('input') `
  border: none;
  outline: none;
  flex: 1;
`;
const CalendarMenu = (0, styled_1.default)('div') `
  display: flex;
  background: ${p => p.theme.background};
  position: absolute;
  left: 0;
  border: 1px solid ${p => p.theme.border};
  border-top: none;
  z-index: ${p => p.theme.zIndex.dropdownAutocomplete.menu};
  margin-top: -1px;

  .rdrMonthAndYearWrapper {
    height: 50px;
    padding-top: 0;
  }
`;
const CalendarIcon = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: center;
  padding: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=datePickerField.jsx.map