Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const analytics_1 = require("app/utils/analytics");
const replaceRouterParams_1 = (0, tslib_1.__importDefault)(require("app/utils/replaceRouterParams"));
const settingsNavItem_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsNavItem"));
const SettingsNavigationGroup = (props) => {
    const { organization, project, name, items } = props;
    const navLinks = items.map(({ path, title, index, show, badge, id, recordAnalytics }) => {
        if (typeof show === 'function' && !show(props)) {
            return null;
        }
        if (typeof show !== 'undefined' && !show) {
            return null;
        }
        const badgeResult = typeof badge === 'function' ? badge(props) : null;
        const to = (0, replaceRouterParams_1.default)(path, Object.assign(Object.assign({}, (organization ? { orgId: organization.slug } : {})), (project ? { projectId: project.slug } : {})));
        const handleClick = () => {
            // only call the analytics event if the URL is changing
            if (recordAnalytics && to !== window.location.pathname) {
                (0, analytics_1.trackAnalyticsEvent)({
                    organization_id: organization ? organization.id : null,
                    project_id: project && project.id,
                    eventName: 'Sidebar Item Clicked',
                    eventKey: 'sidebar.item_clicked',
                    sidebar_item_id: id,
                    dest: path,
                });
            }
        };
        return (<settingsNavItem_1.default key={title} to={to} label={title} index={index} badge={badgeResult} id={id} onClick={handleClick}/>);
    });
    if (!navLinks.some(link => link !== null)) {
        return null;
    }
    return (<NavSection data-test-id={name}>
      <SettingsHeading>{name}</SettingsHeading>
      {navLinks}
    </NavSection>);
};
const NavSection = (0, styled_1.default)('div') `
  margin-bottom: 20px;
`;
const SettingsHeading = (0, styled_1.default)('div') `
  color: ${p => p.theme.subText};
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 20px;
`;
exports.default = SettingsNavigationGroup;
//# sourceMappingURL=settingsNavigationGroup.jsx.map