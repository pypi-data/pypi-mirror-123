Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const integrationExternalMappingForm_1 = (0, tslib_1.__importDefault)(require("app/components/integrationExternalMappingForm"));
const integrationExternalMappings_1 = (0, tslib_1.__importDefault)(require("app/components/integrationExternalMappings"));
const locale_1 = require("app/locale");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
class IntegrationExternalUserMappings extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleDelete = (mapping) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization } = this.props;
            const endpoint = `/organizations/${organization.slug}/external-users/${mapping.id}/`;
            try {
                yield this.api.requestPromise(endpoint, {
                    method: 'DELETE',
                });
                // remove config and update state
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Deletion successful'));
                this.fetchData();
            }
            catch (_a) {
                // no 4xx errors should happen on delete
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('An error occurred'));
            }
        });
        this.handleSubmitSuccess = () => {
            // Don't bother updating state. The info is in array of objects for each object in another array of objects.
            // Easier and less error-prone to re-fetch the data and re-calculate state.
            this.fetchData();
        };
        this.openModal = (mapping) => {
            const { organization, integration } = this.props;
            (0, modal_1.openModal)(({ Body, Header, closeModal }) => (<react_1.Fragment>
        <Header closeButton>{(0, locale_1.t)('Configure External User Mapping')}</Header>
        <Body>
          <integrationExternalMappingForm_1.default organization={organization} integration={integration} onSubmitSuccess={() => {
                    this.handleSubmitSuccess();
                    closeModal();
                }} mapping={mapping} sentryNamesMapper={this.sentryNamesMapper} type="user" url={`/organizations/${organization.slug}/members/`} onCancel={closeModal} baseEndpoint={`/organizations/${organization.slug}/external-users/`}/>
        </Body>
      </react_1.Fragment>));
        };
    }
    getEndpoints() {
        const { organization } = this.props;
        return [
            [
                'members',
                `/organizations/${organization.slug}/members/`,
                { query: { query: 'hasExternalUsers:true', expand: 'externalUsers' } },
            ],
        ];
    }
    get mappings() {
        const { integration } = this.props;
        const { members } = this.state;
        const externalUserMappings = members.reduce((acc, member) => {
            const { externalUsers, user } = member;
            acc.push(...externalUsers
                .filter(externalUser => externalUser.provider === integration.provider.key)
                .map(externalUser => (Object.assign(Object.assign({}, externalUser), { sentryName: user.name }))));
            return acc;
        }, []);
        return externalUserMappings.sort((a, b) => parseInt(a.id, 10) - parseInt(b.id, 10));
    }
    sentryNamesMapper(members) {
        return members
            .filter(member => member.user)
            .map(({ user: { id }, email, name }) => {
            const label = email !== name ? `${name} - ${email}` : `${email}`;
            return { id, name: label };
        });
    }
    renderBody() {
        const { integration } = this.props;
        return (<react_1.Fragment>
        <integrationExternalMappings_1.default integration={integration} type="user" mappings={this.mappings} onCreateOrEdit={this.openModal} onDelete={this.handleDelete}/>
      </react_1.Fragment>);
    }
}
exports.default = (0, withOrganization_1.default)(IntegrationExternalUserMappings);
//# sourceMappingURL=integrationExternalUserMappings.jsx.map