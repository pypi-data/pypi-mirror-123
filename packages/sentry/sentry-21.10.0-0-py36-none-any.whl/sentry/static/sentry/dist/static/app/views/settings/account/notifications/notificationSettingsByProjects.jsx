Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importDefault)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const constants_1 = require("app/views/settings/account/notifications/constants");
const utils_2 = require("app/views/settings/account/notifications/utils");
const defaultSearchBar_1 = require("app/views/settings/components/defaultSearchBar");
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
class NotificationSettingsByProjects extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        /**
         * Check the notification settings for how many projects there are.
         */
        this.getProjectCount = () => {
            var _a;
            const { notificationType, notificationSettings } = this.props;
            return Object.values(((_a = notificationSettings[notificationType]) === null || _a === void 0 ? void 0 : _a.project) || {}).length;
        };
        /**
         * The UI expects projects to be grouped by organization but can also use
         * this function to make a single group with all organizations.
         */
        this.getGroupedProjects = () => {
            const { projects: stateProjects } = this.state;
            return Object.fromEntries(Object.values((0, utils_2.groupByOrganization)((0, utils_1.sortProjects)(stateProjects))).map(({ organization, projects }) => [`${organization.name} Projects`, projects]));
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { projects: [] });
    }
    getEndpoints() {
        return [['projects', '/projects/']];
    }
    renderBody() {
        const { notificationType, notificationSettings, onChange } = this.props;
        const { projects, projectsPageLinks } = this.state;
        const canSearch = this.getProjectCount() >= constants_1.MIN_PROJECTS_FOR_SEARCH;
        const shouldPaginate = projects.length >= constants_1.MIN_PROJECTS_FOR_PAGINATION;
        const renderSearch = ({ defaultSearchBar }) => (<StyledSearchWrapper>{defaultSearchBar}</StyledSearchWrapper>);
        return (<react_1.default.Fragment>
        {canSearch &&
                this.renderSearchInput({
                    stateKey: 'projects',
                    url: '/projects/',
                    placeholder: (0, locale_1.t)('Search Projects'),
                    children: renderSearch,
                })}
        <form_1.default saveOnBlur apiMethod="PUT" apiEndpoint="/users/me/notification-settings/" initialData={(0, utils_2.getParentData)(notificationType, notificationSettings, projects)}>
          {projects.length === 0 ? (<emptyMessage_1.default>{(0, locale_1.t)('No projects found')}</emptyMessage_1.default>) : (Object.entries(this.getGroupedProjects()).map(([groupTitle, parents]) => (<jsonForm_1.default collapsible key={groupTitle} title={groupTitle} fields={parents.map(parent => (0, utils_2.getParentField)(notificationType, notificationSettings, parent, onChange))}/>)))}
        </form_1.default>
        {canSearch && shouldPaginate && (<pagination_1.default pageLinks={projectsPageLinks} {...this.props}/>)}
      </react_1.default.Fragment>);
    }
}
exports.default = NotificationSettingsByProjects;
const StyledSearchWrapper = (0, styled_1.default)(defaultSearchBar_1.SearchWrapper) `
  * {
    width: 100%;
  }
`;
//# sourceMappingURL=notificationSettingsByProjects.jsx.map