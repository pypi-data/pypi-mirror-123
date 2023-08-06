Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const inputField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/inputField"));
const types_1 = require("../../types");
const utils_2 = require("../../utils");
const sourceSuggestionExamples_1 = (0, tslib_1.__importDefault)(require("./sourceSuggestionExamples"));
const defaultHelp = (0, locale_1.t)('Where to look. In the simplest case this can be an attribute name.');
class SourceField extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            suggestions: [],
            fieldValues: [],
            activeSuggestion: 0,
            showSuggestions: false,
            hideCaret: false,
            help: defaultHelp,
        };
        this.selectorField = React.createRef();
        this.suggestionList = React.createRef();
        this.handleChange = (value) => {
            this.loadFieldValues(value);
            this.props.onChange(value);
        };
        this.handleClickOutside = () => {
            this.setState({
                showSuggestions: false,
                hideCaret: false,
            });
        };
        this.handleClickSuggestionItem = (suggestion) => () => {
            const fieldValues = this.getNewFieldValues(suggestion);
            this.setState({
                fieldValues,
                activeSuggestion: 0,
                showSuggestions: false,
                hideCaret: false,
            }, this.changeParentValue);
        };
        this.handleKeyDown = (_value, event) => {
            event.persist();
            const { keyCode } = event;
            const { activeSuggestion, suggestions } = this.state;
            if (keyCode === 8 || keyCode === 32) {
                this.toggleSuggestions(true);
                return;
            }
            if (keyCode === 13) {
                this.handleClickSuggestionItem(suggestions[activeSuggestion])();
                return;
            }
            if (keyCode === 38) {
                if (activeSuggestion === 0) {
                    return;
                }
                this.setState({ activeSuggestion: activeSuggestion - 1 }, () => {
                    this.scrollToSuggestion();
                });
                return;
            }
            if (keyCode === 40) {
                if (activeSuggestion === suggestions.length - 1) {
                    return;
                }
                this.setState({ activeSuggestion: activeSuggestion + 1 }, () => {
                    this.scrollToSuggestion();
                });
                return;
            }
        };
        this.handleFocus = () => {
            this.toggleSuggestions(true);
        };
    }
    componentDidMount() {
        this.loadFieldValues(this.props.value);
        this.toggleSuggestions(false);
    }
    componentDidUpdate(prevProps) {
        if (prevProps.suggestions !== this.props.suggestions) {
            this.loadFieldValues(this.props.value);
            this.toggleSuggestions(false);
        }
        if (prevProps.isRegExMatchesSelected !== this.props.isRegExMatchesSelected ||
            prevProps.value !== this.props.value) {
            this.checkPossiblyRegExMatchExpression(this.props.value);
        }
    }
    getAllSuggestions() {
        return [...this.getValueSuggestions(), ...utils_2.unarySuggestions, ...utils_2.binarySuggestions];
    }
    getValueSuggestions() {
        return this.props.suggestions || [];
    }
    getFilteredSuggestions(value, type) {
        let valuesToBeFiltered = [];
        switch (type) {
            case types_1.SourceSuggestionType.BINARY: {
                valuesToBeFiltered = utils_2.binarySuggestions;
                break;
            }
            case types_1.SourceSuggestionType.VALUE: {
                valuesToBeFiltered = this.getValueSuggestions();
                break;
            }
            case types_1.SourceSuggestionType.UNARY: {
                valuesToBeFiltered = utils_2.unarySuggestions;
                break;
            }
            default: {
                valuesToBeFiltered = [...this.getValueSuggestions(), ...utils_2.unarySuggestions];
            }
        }
        const filteredSuggestions = valuesToBeFiltered.filter(s => s.value.toLowerCase().indexOf(value.toLowerCase()) > -1);
        return filteredSuggestions;
    }
    getNewSuggestions(fieldValues) {
        const lastFieldValue = fieldValues[fieldValues.length - 1];
        const penultimateFieldValue = fieldValues[fieldValues.length - 2];
        if (Array.isArray(lastFieldValue)) {
            // recursion
            return this.getNewSuggestions(lastFieldValue);
        }
        if (Array.isArray(penultimateFieldValue)) {
            if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'binary') {
                // returns filtered values
                return this.getFilteredSuggestions(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value, types_1.SourceSuggestionType.VALUE);
            }
            // returns all binaries without any filter
            return this.getFilteredSuggestions('', types_1.SourceSuggestionType.BINARY);
        }
        if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'value' && (penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.type) === 'unary') {
            // returns filtered values
            return this.getFilteredSuggestions(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value, types_1.SourceSuggestionType.VALUE);
        }
        if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'unary') {
            // returns all values without any filter
            return this.getFilteredSuggestions('', types_1.SourceSuggestionType.VALUE);
        }
        if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'string' && (penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.type) === 'value') {
            // returns all binaries without any filter
            return this.getFilteredSuggestions('', types_1.SourceSuggestionType.BINARY);
        }
        if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'string' &&
            (penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.type) === 'string' &&
            !(penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.value)) {
            // returns all values without any filter
            return this.getFilteredSuggestions('', types_1.SourceSuggestionType.STRING);
        }
        if (((penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.type) === 'string' && !(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value)) ||
            ((penultimateFieldValue === null || penultimateFieldValue === void 0 ? void 0 : penultimateFieldValue.type) === 'value' && !(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value)) ||
            (lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'binary') {
            // returns filtered binaries
            return this.getFilteredSuggestions(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value, types_1.SourceSuggestionType.BINARY);
        }
        return this.getFilteredSuggestions(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value, lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type);
    }
    loadFieldValues(newValue) {
        const fieldValues = [];
        const splittedValue = newValue.split(' ');
        for (const splittedValueIndex in splittedValue) {
            const value = splittedValue[splittedValueIndex];
            const lastFieldValue = fieldValues[fieldValues.length - 1];
            if (lastFieldValue &&
                !Array.isArray(lastFieldValue) &&
                !lastFieldValue.value &&
                !value) {
                continue;
            }
            if (value.includes('!') && !!value.split('!')[1]) {
                const valueAfterUnaryOperator = value.split('!')[1];
                const selector = this.getAllSuggestions().find(s => s.value === valueAfterUnaryOperator);
                if (!selector) {
                    fieldValues.push([
                        utils_2.unarySuggestions[0],
                        { type: types_1.SourceSuggestionType.STRING, value: valueAfterUnaryOperator },
                    ]);
                    continue;
                }
                fieldValues.push([utils_2.unarySuggestions[0], selector]);
                continue;
            }
            const selector = this.getAllSuggestions().find(s => s.value === value);
            if (selector) {
                fieldValues.push(selector);
                continue;
            }
            fieldValues.push({ type: types_1.SourceSuggestionType.STRING, value });
        }
        const filteredSuggestions = this.getNewSuggestions(fieldValues);
        this.setState({
            fieldValues,
            activeSuggestion: 0,
            suggestions: filteredSuggestions,
        });
    }
    scrollToSuggestion() {
        var _a, _b;
        const { activeSuggestion, hideCaret } = this.state;
        (_b = (_a = this.suggestionList) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.children[activeSuggestion].scrollIntoView({
            behavior: 'smooth',
            block: 'nearest',
            inline: 'start',
        });
        if (!hideCaret) {
            this.setState({
                hideCaret: true,
            });
        }
    }
    changeParentValue() {
        var _a, _b, _c, _d, _e, _f;
        const { onChange } = this.props;
        const { fieldValues } = this.state;
        const newValue = [];
        for (const index in fieldValues) {
            const fieldValue = fieldValues[index];
            if (Array.isArray(fieldValue)) {
                if (((_a = fieldValue[0]) === null || _a === void 0 ? void 0 : _a.value) || ((_b = fieldValue[1]) === null || _b === void 0 ? void 0 : _b.value)) {
                    newValue.push(`${(_d = (_c = fieldValue[0]) === null || _c === void 0 ? void 0 : _c.value) !== null && _d !== void 0 ? _d : ''}${(_f = (_e = fieldValue[1]) === null || _e === void 0 ? void 0 : _e.value) !== null && _f !== void 0 ? _f : ''}`);
                }
                continue;
            }
            newValue.push(fieldValue.value);
        }
        onChange(newValue.join(' '));
    }
    getNewFieldValues(suggestion) {
        const fieldValues = [...this.state.fieldValues];
        const lastFieldValue = fieldValues[fieldValues.length - 1];
        if (!(0, utils_1.defined)(lastFieldValue)) {
            return [suggestion];
        }
        if (Array.isArray(lastFieldValue)) {
            fieldValues[fieldValues.length - 1] = [lastFieldValue[0], suggestion];
            return fieldValues;
        }
        if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'unary') {
            fieldValues[fieldValues.length - 1] = [lastFieldValue, suggestion];
        }
        if ((lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.type) === 'string' && !(lastFieldValue === null || lastFieldValue === void 0 ? void 0 : lastFieldValue.value)) {
            fieldValues[fieldValues.length - 1] = suggestion;
        }
        return fieldValues;
    }
    checkPossiblyRegExMatchExpression(value) {
        const { isRegExMatchesSelected } = this.props;
        const { help } = this.state;
        if (isRegExMatchesSelected) {
            if (help) {
                this.setState({ help: '' });
            }
            return;
        }
        const isMaybeRegExp = RegExp('^/.*/g?$').test(value);
        if (help) {
            if (!isMaybeRegExp) {
                this.setState({
                    help: defaultHelp,
                });
            }
            return;
        }
        if (isMaybeRegExp) {
            this.setState({
                help: (0, locale_1.t)("You might want to change Data Type's value to 'Regex matches'"),
            });
        }
    }
    toggleSuggestions(showSuggestions) {
        this.setState({ showSuggestions });
    }
    render() {
        const { error, value, onBlur } = this.props;
        const { showSuggestions, suggestions, activeSuggestion, hideCaret, help } = this.state;
        return (<Wrapper ref={this.selectorField} hideCaret={hideCaret}>
        <StyledInput data-test-id="source-field" type="text" label={(0, locale_1.t)('Source')} name="source" placeholder={(0, locale_1.t)('Enter a custom attribute, variable or header name')} onChange={this.handleChange} autoComplete="off" value={value} error={error} help={help} onKeyDown={this.handleKeyDown} onBlur={onBlur} onFocus={this.handleFocus} inline={false} flexibleControlStateSize stacked required showHelpInTooltip/>
        {showSuggestions && suggestions.length > 0 && (<React.Fragment>
            <Suggestions ref={this.suggestionList} error={error} data-test-id="source-suggestions">
              {suggestions.slice(0, 50).map((suggestion, index) => (<Suggestion key={suggestion.value} onClick={this.handleClickSuggestionItem(suggestion)} active={index === activeSuggestion} tabIndex={-1}>
                  <textOverflow_1.default>{suggestion.value}</textOverflow_1.default>
                  {suggestion.description && (<SuggestionDescription>
                      (<textOverflow_1.default>{suggestion.description}</textOverflow_1.default>)
                    </SuggestionDescription>)}
                  {suggestion.examples && suggestion.examples.length > 0 && (<sourceSuggestionExamples_1.default examples={suggestion.examples} sourceName={suggestion.value}/>)}
                </Suggestion>))}
            </Suggestions>
            <SuggestionsOverlay onClick={this.handleClickOutside}/>
          </React.Fragment>)}
      </Wrapper>);
    }
}
exports.default = SourceField;
const Wrapper = (0, styled_1.default)('div') `
  position: relative;
  width: 100%;
  ${p => p.hideCaret && `caret-color: transparent;`}
`;
const StyledInput = (0, styled_1.default)(inputField_1.default) `
  z-index: 1002;
  :focus {
    outline: none;
  }
`;
const Suggestions = (0, styled_1.default)('ul') `
  position: absolute;
  width: ${p => (p.error ? 'calc(100% - 34px)' : '100%')};
  padding-left: 0;
  list-style: none;
  margin-bottom: 0;
  box-shadow: 0 2px 0 rgba(37, 11, 54, 0.04);
  border: 1px solid ${p => p.theme.border};
  border-radius: 0 0 ${(0, space_1.default)(0.5)} ${(0, space_1.default)(0.5)};
  background: ${p => p.theme.background};
  top: 63px;
  left: 0;
  z-index: 1002;
  overflow: hidden;
  max-height: 200px;
  overflow-y: auto;
`;
const Suggestion = (0, styled_1.default)('li') `
  display: grid;
  grid-template-columns: auto 1fr max-content;
  grid-gap: ${(0, space_1.default)(1)};
  border-bottom: 1px solid ${p => p.theme.border};
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  font-size: ${p => p.theme.fontSizeMedium};
  cursor: pointer;
  background: ${p => (p.active ? p.theme.backgroundSecondary : p.theme.background)};
  :hover {
    background: ${p => p.active ? p.theme.backgroundSecondary : p.theme.backgroundSecondary};
  }
`;
const SuggestionDescription = (0, styled_1.default)('div') `
  display: flex;
  overflow: hidden;
  color: ${p => p.theme.gray300};
`;
const SuggestionsOverlay = (0, styled_1.default)('div') `
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1001;
`;
//# sourceMappingURL=sourceField.jsx.map