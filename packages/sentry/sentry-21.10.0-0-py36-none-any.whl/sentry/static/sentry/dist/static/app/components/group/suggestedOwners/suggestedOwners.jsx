Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const group_1 = require("app/actionCreators/group");
const prompts_1 = require("app/actionCreators/prompts");
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const promptIsDismissed_1 = require("app/utils/promptIsDismissed");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withCommitters_1 = (0, tslib_1.__importDefault)(require("app/utils/withCommitters"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const findMatchedRules_1 = require("./findMatchedRules");
const ownershipRules_1 = require("./ownershipRules");
const suggestedAssignees_1 = require("./suggestedAssignees");
class SuggestedOwners extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleCTAClose = () => {
            const { api, organization, project } = this.props;
            (0, prompts_1.promptsUpdate)(api, {
                organizationId: organization.id,
                projectId: project.id,
                feature: 'code_owners',
                status: 'dismissed',
            });
            this.setState({ isDismissed: true }, () => (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.dismissed_code_owners_prompt', {
                view: 'stacktrace_issue_details',
                project_id: project.id,
                organization,
            }));
        };
        this.handleAssign = (actor) => () => {
            if (actor.id === undefined) {
                return;
            }
            const { event } = this.props;
            if (actor.type === 'user') {
                // TODO(ts): `event` here may not be 100% correct
                // in this case groupID should always exist on event
                // since this is only used in Issue Details
                (0, group_1.assignToUser)({
                    id: event.groupID,
                    user: actor,
                    assignedBy: 'suggested_assignee',
                });
            }
            if (actor.type === 'team') {
                (0, group_1.assignToActor)({
                    id: event.groupID,
                    actor,
                    assignedBy: 'suggested_assignee',
                });
            }
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { event: { rules: [], owners: [] }, codeowners: [], isDismissed: true });
    }
    getEndpoints() {
        const { project, organization, event } = this.props;
        const endpoints = [
            [
                'event_owners',
                `/projects/${organization.slug}/${project.slug}/events/${event.id}/owners/`,
            ],
        ];
        if (organization.features.includes('integrations-codeowners')) {
            endpoints.push([
                `codeowners`,
                `/projects/${organization.slug}/${project.slug}/codeowners/`,
            ]);
        }
        return endpoints;
    }
    componentDidMount() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            yield this.checkCodeOwnersPrompt();
        });
    }
    componentDidUpdate(prevProps) {
        if (this.props.event && prevProps.event) {
            if (this.props.event.id !== prevProps.event.id) {
                // two events, with different IDs
                this.reloadData();
            }
            return;
        }
        if (this.props.event) {
            // going from having no event to having an event
            this.reloadData();
        }
    }
    checkCodeOwnersPrompt() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, project } = this.props;
            if (!organization.features.includes('integrations-codeowners')) {
                return;
            }
            // check our prompt backend
            const promptData = yield (0, prompts_1.promptsCheck)(api, {
                organizationId: organization.id,
                projectId: project.id,
                feature: 'code_owners',
            });
            const isDismissed = (0, promptIsDismissed_1.promptIsDismissed)(promptData, 30);
            this.setState({ isDismissed }, () => {
                if (!isDismissed) {
                    // now record the results
                    (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.show_code_owners_prompt', {
                        view: 'stacktrace_issue_details',
                        project_id: project.id,
                        organization,
                    }, { startSession: true });
                }
            });
        });
    }
    /**
     * Combine the commiter and ownership data into a single array, merging
     * users who are both owners based on having commits, and owners matching
     * project ownership rules into one array.
     *
     * The return array will include objects of the format:
     *
     * {
     *   actor: <
     *    type,              # Either user or team
     *    SentryTypes.User,  # API expanded user object
     *    {email, id, name}  # Sentry user which is *not* expanded
     *    {email, name}      # Unidentified user (from commits)
     *    {id, name},        # Sentry team (check `type`)
     *   >,
     *
     *   # One or both of commits and rules will be present
     *
     *   commits: [...]  # List of commits made by this owner
     *   rules:   [...]  # Project rules matched for this owner
     * }
     */
    getOwnerList() {
        var _a;
        const committers = (_a = this.props.committers) !== null && _a !== void 0 ? _a : [];
        const owners = committers.map(commiter => ({
            actor: Object.assign(Object.assign({}, commiter.author), { type: 'user' }),
            commits: commiter.commits,
        }));
        this.state.event_owners.owners.forEach(owner => {
            const normalizedOwner = {
                actor: owner,
                rules: (0, findMatchedRules_1.findMatchedRules)(this.state.event_owners.rules || [], owner),
            };
            const existingIdx = owners.findIndex(o => committers.length === 0 ? o.actor === owner : o.actor.email === owner.email);
            if (existingIdx > -1) {
                owners[existingIdx] = Object.assign(Object.assign({}, normalizedOwner), owners[existingIdx]);
                return;
            }
            owners.push(normalizedOwner);
        });
        return owners;
    }
    renderBody() {
        const { organization, project, group } = this.props;
        const { codeowners, isDismissed } = this.state;
        const owners = this.getOwnerList();
        return (<React.Fragment>
        {owners.length > 0 && (<suggestedAssignees_1.SuggestedAssignees owners={owners} onAssign={this.handleAssign}/>)}
        <ownershipRules_1.OwnershipRules issueId={group.id} project={project} organization={organization} codeowners={codeowners} isDismissed={isDismissed} handleCTAClose={this.handleCTAClose}/>
      </React.Fragment>);
    }
}
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)((0, withCommitters_1.default)(SuggestedOwners)));
//# sourceMappingURL=suggestedOwners.jsx.map