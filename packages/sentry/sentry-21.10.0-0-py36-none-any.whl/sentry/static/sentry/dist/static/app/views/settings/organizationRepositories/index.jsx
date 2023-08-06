Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const locale_1 = require("app/locale");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const organizationRepositories_1 = (0, tslib_1.__importDefault)(require("./organizationRepositories"));
class OrganizationRepositoriesContainer extends asyncView_1.default {
    constructor() {
        super(...arguments);
        // Callback used by child component to signal state change
        this.onRepositoryChange = (data) => {
            const itemList = this.state.itemList;
            itemList === null || itemList === void 0 ? void 0 : itemList.forEach(item => {
                if (item.id === data.id) {
                    item.status = data.status;
                }
            });
            this.setState({ itemList });
        };
    }
    getEndpoints() {
        const { orgId } = this.props.params;
        return [['itemList', `/organizations/${orgId}/repos/`, { query: { status: '' } }]];
    }
    getTitle() {
        const { orgId } = this.props.params;
        return (0, routeTitle_1.default)((0, locale_1.t)('Repositories'), orgId, false);
    }
    renderBody() {
        const { itemList, itemListPageLinks } = this.state;
        return (<react_1.Fragment>
        <organizationRepositories_1.default {...this.props} itemList={itemList} api={this.api} onRepositoryChange={this.onRepositoryChange}/>
        {itemListPageLinks && (<pagination_1.default pageLinks={itemListPageLinks} {...this.props}/>)}
      </react_1.Fragment>);
    }
}
exports.default = OrganizationRepositoriesContainer;
//# sourceMappingURL=index.jsx.map