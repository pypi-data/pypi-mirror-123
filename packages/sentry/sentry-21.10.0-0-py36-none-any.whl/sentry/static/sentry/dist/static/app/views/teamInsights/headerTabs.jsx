Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const featureBadge_1 = (0, tslib_1.__importDefault)(require("app/components/featureBadge"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const locale_1 = require("app/locale");
function HeaderTabs({ organization, activeTab }) {
    return (<Layout.HeaderNavTabs underlined>
      <li className={`${activeTab === 'projects' ? 'active' : ''}`}>
        <link_1.default to={`/organizations/${organization.slug}/projects/`}>{(0, locale_1.t)('Overview')}</link_1.default>
      </li>
      <li className={`${activeTab === 'teamInsights' ? 'active' : ''}`}>
        <link_1.default to={`/organizations/${organization.slug}/teamInsights/`}>
          {(0, locale_1.t)('Reports')}
          <featureBadge_1.default type="alpha"/>
        </link_1.default>
      </li>
    </Layout.HeaderNavTabs>);
}
exports.default = HeaderTabs;
//# sourceMappingURL=headerTabs.jsx.map