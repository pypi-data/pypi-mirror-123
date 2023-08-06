Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const grouping_1 = (0, tslib_1.__importDefault)(require("./grouping"));
function GroupingContainer({ organization, location, group, router, project }) {
    return (<feature_1.default features={['grouping-tree-ui']} organization={organization} renderDisabled={() => (<organization_1.PageContent>
          <alert_1.default type="warning">{(0, locale_1.t)("You don't have access to this feature")}</alert_1.default>
        </organization_1.PageContent>)}>
      <grouping_1.default location={location} groupId={group.id} organization={organization} router={router} projSlug={project.slug}/>
    </feature_1.default>);
}
exports.default = (0, withOrganization_1.default)(GroupingContainer);
//# sourceMappingURL=index.jsx.map