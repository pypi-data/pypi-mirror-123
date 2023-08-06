Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const panel_1 = (0, tslib_1.__importDefault)(require("app/components/panels/panel"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const BODY_CLASSES = ['narrow'];
class Layout extends React.Component {
    componentDidMount() {
        document.body.classList.add(...BODY_CLASSES);
    }
    componentWillUnmount() {
        document.body.classList.remove(...BODY_CLASSES);
    }
    render() {
        const { children } = this.props;
        return (<div className="app">
        <AuthContainer>
          <div className="pattern-bg"/>
          <AuthPanel>
            <AuthSidebar>
              <SentryButton />
            </AuthSidebar>
            <div>{children}</div>
          </AuthPanel>
        </AuthContainer>
      </div>);
    }
}
const AuthContainer = (0, styled_1.default)('div') `
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 5vh;
`;
const AuthPanel = (0, styled_1.default)(panel_1.default) `
  min-width: 550px;
  display: inline-grid;
  grid-template-columns: 60px 1fr;
`;
const AuthSidebar = (0, styled_1.default)('div') `
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: ${(0, space_1.default)(3)};
  border-radius: ${p => p.theme.borderRadius} 0 0 ${p => p.theme.borderRadius};
  margin: -1px;
  margin-right: 0;
  background: #564f64;
  background-image: linear-gradient(
    -180deg,
    rgba(52, 44, 62, 0) 0%,
    rgba(52, 44, 62, 0.5) 100%
  );
`;
const SentryButton = (0, styled_1.default)((p) => (<link_1.default to="/" {...p}>
      <icons_1.IconSentry size="24px"/>
    </link_1.default>)) `
  color: #fff;

  &:hover,
  &:focus {
    color: #fff;
  }
`;
exports.default = Layout;
//# sourceMappingURL=layout.jsx.map