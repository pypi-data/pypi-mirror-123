Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const indicator_1 = require("app/actionCreators/indicator");
const api_1 = require("app/api");
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const defaultProps = {
    value: '',
};
class IssueListTagFilter extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            query: '',
            isLoading: false,
            value: this.props.value,
            textValue: this.props.value,
        };
        this.api = new api_1.Client();
        this.handleLoadOptions = () => {
            const { tag, tagValueLoader } = this.props;
            const { textValue } = this.state;
            if (tag.isInput || tag.predefined) {
                return;
            }
            if (!this.api) {
                return;
            }
            this.setState({
                isLoading: true,
            });
            tagValueLoader(tag.key, textValue)
                .then(resp => {
                this.setState({
                    isLoading: false,
                    options: Object.values(resp).map(({ value }) => ({
                        value,
                        label: value,
                    })),
                });
            })
                .catch(() => {
                // TODO(billy): This endpoint seems to timeout a lot,
                // should we log these errors into datadog?
                (0, indicator_1.addErrorMessage)((0, locale_1.tct)('Unable to retrieve values for tag [tagName]', {
                    tagName: textValue,
                }));
            });
        };
        this.handleChangeInput = (e) => {
            const value = e.target.value;
            this.setState({
                textValue: value,
            });
            this.debouncedTextChange(value);
        };
        this.debouncedTextChange = (0, debounce_1.default)(text => {
            this.handleChange(text);
        }, 150);
        this.handleOpenMenu = () => {
            if (this.props.tag.predefined) {
                return;
            }
            this.setState({
                isLoading: true,
            }, this.handleLoadOptions);
        };
        this.handleChangeSelect = (valueObj) => {
            const value = valueObj ? valueObj.value : null;
            this.handleChange(value);
        };
        this.handleChangeSelectInput = (value) => {
            this.setState({
                textValue: value,
            }, this.handleLoadOptions);
        };
        this.handleChange = (value) => {
            const { onSelect, tag } = this.props;
            this.setState({
                value,
            }, () => {
                onSelect && onSelect(tag, value);
            });
        };
    }
    UNSAFE_componentWillReceiveProps(nextProps) {
        if (nextProps.value !== this.state.value) {
            this.setState({
                value: nextProps.value,
                textValue: nextProps.value,
            });
        }
    }
    componentWillUnmount() {
        if (!this.api) {
            return;
        }
        this.api.clear();
    }
    render() {
        const { tag } = this.props;
        const { options, isLoading } = this.state;
        return (<StreamTagFilter>
        <StyledHeader>{tag.key}</StyledHeader>

        {!!tag.isInput && (<input className="form-control" type="text" value={this.state.textValue} onChange={this.handleChangeInput}/>)}

        {!tag.isInput && (<selectControl_1.default clearable aria-label={tag.key} placeholder="--" loadingMessage={() => (0, locale_1.t)('Loading\u2026')} value={this.state.value} onChange={this.handleChangeSelect} isLoading={isLoading} onInputChange={this.handleChangeSelectInput} onFocus={this.handleOpenMenu} noResultsText={isLoading ? (0, locale_1.t)('Loading\u2026') : (0, locale_1.t)('No results found')} options={tag.predefined
                    ? tag.values &&
                        tag.values.map(value => ({
                            value,
                            label: value,
                        }))
                    : options}/>)}
      </StreamTagFilter>);
    }
}
IssueListTagFilter.defaultProps = defaultProps;
exports.default = IssueListTagFilter;
const StreamTagFilter = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(2)};
`;
const StyledHeader = (0, styled_1.default)('h6') `
  color: ${p => p.theme.subText};
  margin-bottom: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=tagFilter.jsx.map