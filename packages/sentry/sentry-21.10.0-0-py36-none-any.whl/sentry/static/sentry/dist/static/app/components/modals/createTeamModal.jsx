Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const teams_1 = require("app/actionCreators/teams");
const createTeamForm_1 = (0, tslib_1.__importDefault)(require("app/components/teams/createTeamForm"));
const locale_1 = require("app/locale");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class CreateTeamModal extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleSubmit = (data, onSuccess, onError) => {
            const { organization, api } = this.props;
            (0, teams_1.createTeam)(api, data, { orgId: organization.slug })
                .then((resp) => {
                this.handleSuccess(resp);
                onSuccess(resp);
            })
                .catch((err) => {
                onError(err);
            });
        };
    }
    handleSuccess(team) {
        if (this.props.onClose) {
            this.props.onClose(team);
        }
        this.props.closeModal();
    }
    render() {
        const _a = this.props, { Body, Header } = _a, props = (0, tslib_1.__rest)(_a, ["Body", "Header"]);
        return (<react_1.Fragment>
        <Header closeButton>{(0, locale_1.t)('Create Team')}</Header>
        <Body>
          <createTeamForm_1.default {...props} onSubmit={this.handleSubmit}/>
        </Body>
      </react_1.Fragment>);
    }
}
exports.default = (0, withApi_1.default)(CreateTeamModal);
//# sourceMappingURL=createTeamModal.jsx.map