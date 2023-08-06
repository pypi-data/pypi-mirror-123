Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const rules_1 = (0, tslib_1.__importDefault)(require("./rules"));
class OrganizationRules extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isCollapsed: true,
        };
        this.rulesRef = (0, react_1.createRef)();
        this.handleToggleCollapsed = () => {
            this.setState(prevState => ({
                isCollapsed: !prevState.isCollapsed,
            }));
        };
    }
    componentDidUpdate() {
        this.loadContentHeight();
    }
    loadContentHeight() {
        var _a;
        if (!this.state.contentHeight) {
            const contentHeight = (_a = this.rulesRef.current) === null || _a === void 0 ? void 0 : _a.offsetHeight;
            if (contentHeight) {
                this.setState({ contentHeight: `${contentHeight}px` });
            }
        }
    }
    render() {
        const { rules } = this.props;
        const { isCollapsed, contentHeight } = this.state;
        if (rules.length === 0) {
            return (<Wrapper>
          {(0, locale_1.t)('There are no data scrubbing rules at the organization level')}
        </Wrapper>);
        }
        return (<Wrapper isCollapsed={isCollapsed} contentHeight={contentHeight}>
        <Header onClick={this.handleToggleCollapsed}>
          <div>{(0, locale_1.t)('Organization Rules')}</div>
          <button_1.default title={isCollapsed
                ? (0, locale_1.t)('Expand Organization Rules')
                : (0, locale_1.t)('Collapse Organization Rules')} icon={<icons_1.IconChevron size="xs" direction={isCollapsed ? 'down' : 'up'}/>} size="xsmall"/>
        </Header>
        <Content>
          <rules_1.default rules={rules} ref={this.rulesRef} disabled/>
        </Content>
      </Wrapper>);
    }
}
exports.default = OrganizationRules;
const Content = (0, styled_1.default)('div') `
  transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;
  height: 0;
  overflow: hidden;
`;
const Header = (0, styled_1.default)('div') `
  cursor: pointer;
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  border-bottom: 1px solid ${p => p.theme.border};
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
`;
const Wrapper = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray200};
  background: ${p => p.theme.backgroundSecondary};
  ${p => !p.contentHeight && `padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)}`};
  ${p => !p.isCollapsed && ` border-bottom: 1px solid ${p.theme.border}`};
  ${p => !p.isCollapsed &&
    p.contentHeight &&
    `
      ${Content} {
        height: ${p.contentHeight};
      }
    `}
`;
//# sourceMappingURL=organizationRules.jsx.map