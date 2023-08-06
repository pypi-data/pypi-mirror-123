Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const locale_1 = require("app/locale");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const auditLogList_1 = (0, tslib_1.__importDefault)(require("./auditLogList"));
// Please keep this list sorted
const EVENT_TYPES = [
    'member.invite',
    'member.add',
    'member.accept-invite',
    'member.remove',
    'member.edit',
    'member.join-team',
    'member.leave-team',
    'member.pending',
    'team.create',
    'team.edit',
    'team.remove',
    'project.create',
    'project.edit',
    'project.remove',
    'project.set-public',
    'project.set-private',
    'project.request-transfer',
    'project.accept-transfer',
    'org.create',
    'org.edit',
    'org.remove',
    'org.restore',
    'tagkey.remove',
    'projectkey.create',
    'projectkey.edit',
    'projectkey.remove',
    'projectkey.enable',
    'projectkey.disable',
    'sso.enable',
    'sso.disable',
    'sso.edit',
    'sso-identity.link',
    'api-key.create',
    'api-key.edit',
    'api-key.remove',
    'rule.create',
    'rule.edit',
    'rule.remove',
    'servicehook.create',
    'servicehook.edit',
    'servicehook.remove',
    'servicehook.enable',
    'servicehook.disable',
    'integration.add',
    'integration.edit',
    'integration.remove',
    'ondemand.edit',
    'trial.started',
    'plan.changed',
    'plan.cancelled',
];
class OrganizationAuditLog extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleEventSelect = (value) => {
            // Dont update if event has not changed
            if (this.props.location.query.event === value) {
                return;
            }
            react_router_1.browserHistory.push({
                pathname: this.props.location.pathname,
                search: `?event=${value}`,
            });
        };
    }
    getEndpoints() {
        return [
            [
                'entryList',
                `/organizations/${this.props.params.orgId}/audit-logs/`,
                {
                    query: this.props.location.query,
                },
            ],
        ];
    }
    getTitle() {
        return (0, routeTitle_1.default)((0, locale_1.t)('Audit Log'), this.props.organization.slug, false);
    }
    renderBody() {
        const currentEventType = this.props.location.query.event;
        return (<auditLogList_1.default entries={this.state.entryList} pageLinks={this.state.entryListPageLinks} eventType={currentEventType} eventTypes={EVENT_TYPES} onEventSelect={this.handleEventSelect} {...this.props}/>);
    }
}
exports.default = (0, withOrganization_1.default)(OrganizationAuditLog);
//# sourceMappingURL=index.jsx.map