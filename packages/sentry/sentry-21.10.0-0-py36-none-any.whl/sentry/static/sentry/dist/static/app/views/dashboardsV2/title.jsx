Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const editableText_1 = (0, tslib_1.__importDefault)(require("app/components/editableText"));
const locale_1 = require("app/locale");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
function DashboardTitle({ dashboard, isEditing, organization, onUpdate }) {
    return (<div>
      {!dashboard ? ((0, locale_1.t)('Dashboards')) : (<editableText_1.default isDisabled={!isEditing} value={organization.features.includes('dashboards-edit') &&
                dashboard.id === 'default-overview'
                ? 'Default Dashboard'
                : dashboard.title} onChange={newTitle => onUpdate(Object.assign(Object.assign({}, dashboard), { title: newTitle }))} errorMessage={(0, locale_1.t)('Please set a title for this dashboard')} successMessage={(0, locale_1.t)('Dashboard title updated successfully')}/>)}
    </div>);
}
exports.default = (0, withOrganization_1.default)(DashboardTitle);
//# sourceMappingURL=title.jsx.map