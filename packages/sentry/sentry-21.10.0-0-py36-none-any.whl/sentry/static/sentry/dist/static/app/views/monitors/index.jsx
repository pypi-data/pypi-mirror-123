Object.defineProperty(exports, "__esModule", { value: true });
exports.MonitorsContainer = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/globalSelectionHeader"));
const organization_1 = require("app/styles/organization");
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const Body = (0, styled_1.default)('div') `
  background-color: ${p => p.theme.backgroundSecondary};
  flex-direction: column;
  flex: 1;
`;
const MonitorsContainer = ({ children }) => (<feature_1.default features={['monitors']} renderDisabled>
    <globalSelectionHeader_1.default showEnvironmentSelector={false} showDateSelector={false} resetParamsOnChange={['cursor']}>
      <organization_1.PageContent>
        <Body>{children}</Body>
      </organization_1.PageContent>
    </globalSelectionHeader_1.default>
  </feature_1.default>);
exports.MonitorsContainer = MonitorsContainer;
exports.default = (0, withGlobalSelection_1.default)(MonitorsContainer);
//# sourceMappingURL=index.jsx.map