Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const prop_types_1 = (0, tslib_1.__importDefault)(require("prop-types"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withLatestContext_1 = (0, tslib_1.__importDefault)(require("app/utils/withLatestContext"));
const scrollToTop_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/scrollToTop"));
class SettingsWrapper extends react_1.Component {
    constructor() {
        super(...arguments);
        // save current context
        this.state = {
            lastAppContext: this.getLastAppContext(),
        };
        this.handleShouldDisableScrollToTop = (location, prevLocation) => {
            var _a, _b;
            // we do not want to scroll to top when user just perform a search
            return (location.pathname === prevLocation.pathname &&
                ((_a = location.query) === null || _a === void 0 ? void 0 : _a.query) !== ((_b = prevLocation.query) === null || _b === void 0 ? void 0 : _b.query));
        };
    }
    getChildContext() {
        return {
            lastAppContext: this.state.lastAppContext,
        };
    }
    getLastAppContext() {
        const { project, organization } = this.props;
        if (!!project) {
            return 'project';
        }
        if (!!organization) {
            return 'organization';
        }
        return null;
    }
    render() {
        const { location, children } = this.props;
        return (<StyledSettingsWrapper>
        <scrollToTop_1.default location={location} disable={this.handleShouldDisableScrollToTop}>
          {children}
        </scrollToTop_1.default>
      </StyledSettingsWrapper>);
    }
}
SettingsWrapper.childContextTypes = {
    lastAppContext: prop_types_1.default.oneOf(['project', 'organization']),
};
exports.default = (0, withLatestContext_1.default)(SettingsWrapper);
const StyledSettingsWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;
  font-size: ${p => p.theme.fontSizeLarge};
  color: ${p => p.theme.textColor};
  margin-bottom: -${(0, space_1.default)(3)}; /* to account for footer margin top */
  line-height: 1;

  .messages-container {
    margin: 0;
  }
`;
//# sourceMappingURL=settingsWrapper.jsx.map