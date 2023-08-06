Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const radioGroup_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/radioGroup"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const model_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/model"));
const userEditForm = {
    title: 'User details',
    fields: [
        {
            name: 'name',
            type: 'string',
            required: true,
            label: (0, locale_1.t)('Name'),
        },
        {
            name: 'username',
            type: 'string',
            required: true,
            label: (0, locale_1.t)('Username'),
            help: (0, locale_1.t)('The username is the unique id of the user in the system'),
        },
        {
            name: 'email',
            type: 'string',
            required: true,
            label: (0, locale_1.t)('Email'),
            help: (0, locale_1.t)('The users primary email address'),
        },
        {
            name: 'isActive',
            type: 'boolean',
            required: true,
            label: (0, locale_1.t)('Active'),
            help: (0, locale_1.t)('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'),
        },
        {
            name: 'isStaff',
            type: 'boolean',
            required: true,
            label: (0, locale_1.t)('Admin'),
            help: (0, locale_1.t)('Designates whether this user can perform administrative functions.'),
        },
        {
            name: 'isSuperuser',
            type: 'boolean',
            required: true,
            label: (0, locale_1.t)('Superuser'),
            help: (0, locale_1.t)('Designates whether this user has all permissions without explicitly assigning them.'),
        },
    ],
};
const REMOVE_BUTTON_LABEL = {
    disable: (0, locale_1.t)('Disable User'),
    delete: (0, locale_1.t)('Permanently Delete User'),
};
class RemoveUserModal extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            deleteType: 'disable',
        };
        this.onRemove = () => {
            this.props.onRemove(this.state.deleteType);
            this.props.closeModal();
        };
    }
    render() {
        const { user } = this.props;
        const { deleteType } = this.state;
        return (<react_1.Fragment>
        <radioGroup_1.default value={deleteType} label={(0, locale_1.t)('Remove user %s', user.email)} onChange={type => this.setState({ deleteType: type })} choices={[
                ['disable', (0, locale_1.t)('Disable the account.')],
                ['delete', (0, locale_1.t)('Permanently remove the user and their data.')],
            ]}/>
        <ModalFooter>
          <button_1.default priority="danger" onClick={this.onRemove}>
            {REMOVE_BUTTON_LABEL[deleteType]}
          </button_1.default>
          <button_1.default onClick={this.props.closeModal}>{(0, locale_1.t)('Cancel')}</button_1.default>
        </ModalFooter>
      </react_1.Fragment>);
    }
}
class AdminUserEdit extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.removeUser = (actionTypes) => actionTypes === 'delete' ? this.deleteUser() : this.deactivateUser();
        this.formModel = new model_1.default();
    }
    get userEndpoint() {
        const { params } = this.props;
        return `/users/${params.id}/`;
    }
    getEndpoints() {
        return [['user', this.userEndpoint]];
    }
    deleteUser() {
        var _a;
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            yield this.api.requestPromise(this.userEndpoint, {
                method: 'DELETE',
                data: { hardDelete: true, organizations: [] },
            });
            (0, indicator_1.addSuccessMessage)((0, locale_1.t)("%s's account has been deleted.", (_a = this.state.user) === null || _a === void 0 ? void 0 : _a.email));
            react_router_1.browserHistory.replace('/manage/users/');
        });
    }
    deactivateUser() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const response = yield this.api.requestPromise(this.userEndpoint, {
                method: 'PUT',
                data: { isActive: false },
            });
            this.setState({ user: response });
            this.formModel.setInitialData(response);
            (0, indicator_1.addSuccessMessage)((0, locale_1.t)("%s's account has been deactivated.", response.email));
        });
    }
    renderBody() {
        const { user } = this.state;
        if (user === null) {
            return null;
        }
        const openDeleteModal = () => (0, modal_1.openModal)(opts => (<RemoveUserModal user={user} onRemove={this.removeUser} {...opts}/>));
        return (<react_1.Fragment>
        <h3>{(0, locale_1.t)('Users')}</h3>
        <p>{(0, locale_1.t)('Editing user: %s', user.email)}</p>
        <form_1.default model={this.formModel} initialData={user} apiMethod="PUT" apiEndpoint={this.userEndpoint} requireChanges onSubmitError={indicator_1.addErrorMessage} onSubmitSuccess={data => {
                this.setState({ user: data });
                (0, indicator_1.addSuccessMessage)('User account updated.');
            }} extraButton={<button_1.default type="button" onClick={openDeleteModal} style={{ marginLeft: (0, space_1.default)(1) }} priority="danger">
              {(0, locale_1.t)('Remove User')}
            </button_1.default>}>
          <jsonForm_1.default forms={[userEditForm]}/>
        </form_1.default>
      </react_1.Fragment>);
    }
}
const ModalFooter = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  grid-gap: ${(0, space_1.default)(1)};
  justify-content: end;
  padding: 20px 30px;
  margin: 20px -30px -30px;
  border-top: 1px solid ${p => p.theme.border};
`;
exports.default = AdminUserEdit;
//# sourceMappingURL=adminUserEdit.jsx.map