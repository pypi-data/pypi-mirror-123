Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const annotatedText_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotatedText"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const REGISTER_VIEWS = [(0, locale_1.t)('Hexadecimal'), (0, locale_1.t)('Numeric')];
class Value extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = { view: 0 };
        this.toggleView = () => {
            this.setState(state => ({ view: (state.view + 1) % REGISTER_VIEWS.length }));
        };
    }
    formatValue() {
        const { value } = this.props;
        const { view } = this.state;
        try {
            const parsed = typeof value === 'string' ? parseInt(value, 16) : value;
            if (isNaN(parsed)) {
                return value;
            }
            switch (view) {
                case 1:
                    return `${parsed}`;
                case 0:
                default:
                    return `0x${('0000000000000000' + parsed.toString(16)).substr(-16)}`;
            }
        }
        catch (_a) {
            return value;
        }
    }
    render() {
        const formattedValue = this.formatValue();
        const { meta } = this.props;
        const { view } = this.state;
        return (<InlinePre data-test-id="frame-registers-value">
        <FixedWidth>
          <annotatedText_1.default value={formattedValue} meta={meta}/>
        </FixedWidth>
        <tooltip_1.default title={REGISTER_VIEWS[view]}>
          <Toggle onClick={this.toggleView} size="xs"/>
        </tooltip_1.default>
      </InlinePre>);
    }
}
exports.default = Value;
const InlinePre = (0, styled_1.default)('pre') `
  display: inline;
`;
const FixedWidth = (0, styled_1.default)('span') `
  width: 11em;
  display: inline-block;
  text-align: right;
  margin-right: 1ex;
`;
const Toggle = (0, styled_1.default)(icons_1.IconSliders) `
  opacity: 0.33;
  cursor: pointer;

  &:hover {
    opacity: 1;
  }
`;
//# sourceMappingURL=value.jsx.map