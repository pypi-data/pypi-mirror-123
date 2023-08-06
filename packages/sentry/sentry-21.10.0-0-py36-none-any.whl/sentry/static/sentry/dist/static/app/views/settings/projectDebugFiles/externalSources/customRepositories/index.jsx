Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
const dropdownAutoComplete_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownAutoComplete"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const panels_1 = require("app/components/panels");
const appStoreConnectContext_1 = (0, tslib_1.__importDefault)(require("app/components/projects/appStoreConnectContext"));
const locale_1 = require("app/locale");
const debugFiles_1 = require("app/types/debugFiles");
const utils_1 = require("app/utils");
const repository_1 = (0, tslib_1.__importDefault)(require("./repository"));
const utils_2 = require("./utils");
const HookedAppStoreConnectItem = (0, hookOrDefault_1.default)({
    hookName: 'component:disabled-app-store-connect-item',
    defaultComponent: ({ children }) => <react_1.Fragment>{children}</react_1.Fragment>,
});
function CustomRepositories({ api, organization, customRepositories: repositories, projSlug, router, location, }) {
    var _a;
    const appStoreConnectContext = (0, react_1.useContext)(appStoreConnectContext_1.default);
    (0, react_1.useEffect)(() => {
        openDebugFileSourceDialog();
    }, [location.query, appStoreConnectContext]);
    const orgSlug = organization.slug;
    const hasAppStoreConnectMultipleFeatureFlag = !!((_a = organization.features) === null || _a === void 0 ? void 0 : _a.includes('app-store-connect-multiple'));
    const hasAppStoreConnectRepo = !!repositories.find(repository => repository.type === debugFiles_1.CustomRepoType.APP_STORE_CONNECT);
    if (!appStoreConnectContext &&
        !utils_2.dropDownItems.find(dropDownItem => dropDownItem.value === debugFiles_1.CustomRepoType.APP_STORE_CONNECT)) {
        utils_2.dropDownItems.push({
            value: debugFiles_1.CustomRepoType.APP_STORE_CONNECT,
            label: utils_2.customRepoTypeLabel[debugFiles_1.CustomRepoType.APP_STORE_CONNECT],
            searchKey: (0, locale_1.t)('apple store connect itunes ios'),
        });
    }
    function openDebugFileSourceDialog() {
        const { customRepository } = location.query;
        if (!customRepository) {
            return;
        }
        const itemIndex = repositories.findIndex(v => v.id === customRepository);
        const item = repositories[itemIndex];
        if (!item) {
            return;
        }
        (0, modal_1.openDebugFileSourceModal)({
            sourceConfig: item,
            sourceType: item.type,
            appStoreConnectContext,
            onSave: updatedItem => persistData({ updatedItem: updatedItem, index: itemIndex }),
            onClose: handleCloseModal,
        });
    }
    function persistData({ updatedItems, updatedItem, index, refresh, }) {
        let items = updatedItems !== null && updatedItems !== void 0 ? updatedItems : [];
        if (updatedItem && (0, utils_1.defined)(index)) {
            items = [...repositories];
            items.splice(index, 1, updatedItem);
        }
        const { successMessage, errorMessage } = (0, utils_2.getRequestMessages)(items.length, repositories.length);
        const symbolSources = JSON.stringify(items.map(utils_2.expandKeys));
        const promise = api.requestPromise(`/projects/${orgSlug}/${projSlug}/`, {
            method: 'PUT',
            data: { symbolSources },
        });
        promise.catch(() => {
            (0, indicator_1.addErrorMessage)(errorMessage);
        });
        promise.then(result => {
            projectActions_1.default.updateSuccess(result);
            (0, indicator_1.addSuccessMessage)(successMessage);
            if (refresh) {
                window.location.reload();
            }
        });
        return promise;
    }
    function handleCloseModal() {
        router.push(Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { customRepository: undefined, revalidateItunesSession: undefined }) }));
    }
    function handleAddRepository(repoType) {
        (0, modal_1.openDebugFileSourceModal)({
            sourceType: repoType,
            onSave: updatedData => persistData({ updatedItems: [...repositories, updatedData] }),
        });
    }
    function handleDeleteRepository(repoId) {
        const newRepositories = [...repositories];
        const index = newRepositories.findIndex(item => item.id === repoId);
        newRepositories.splice(index, 1);
        persistData({
            updatedItems: newRepositories,
            refresh: repositories[index].type === debugFiles_1.CustomRepoType.APP_STORE_CONNECT,
        });
    }
    function handleEditRepository(repoId, revalidateItunesSession) {
        router.push(Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { customRepository: repoId, revalidateItunesSession }) }));
    }
    return (<panels_1.Panel>
      <panels_1.PanelHeader hasButtons>
        {(0, locale_1.t)('Custom Repositories')}
        <dropdownAutoComplete_1.default alignMenu="right" onSelect={item => {
            handleAddRepository(item.value);
        }} items={utils_2.dropDownItems.map(dropDownItem => {
            const disabled = dropDownItem.value === debugFiles_1.CustomRepoType.APP_STORE_CONNECT &&
                hasAppStoreConnectRepo &&
                !hasAppStoreConnectMultipleFeatureFlag;
            return Object.assign(Object.assign({}, dropDownItem), { value: dropDownItem.value, disabled, label: (<HookedAppStoreConnectItem disabled={disabled} onTrialStarted={() => {
                        handleAddRepository(dropDownItem.value);
                    }}>
                  <StyledMenuItem disabled={disabled}>
                    {dropDownItem.label}
                  </StyledMenuItem>
                </HookedAppStoreConnectItem>) });
        })}>
          {({ isOpen }) => (<dropdownButton_1.default isOpen={isOpen} size="small">
              {(0, locale_1.t)('Add Repository')}
            </dropdownButton_1.default>)}
        </dropdownAutoComplete_1.default>
      </panels_1.PanelHeader>
      <panels_1.PanelBody>
        {!repositories.length ? (<emptyStateWarning_1.default>
            <p>{(0, locale_1.t)('No custom repositories configured')}</p>
          </emptyStateWarning_1.default>) : (repositories.map((repository, index) => {
            const repositoryCopy = Object.assign({}, repository);
            if (repositoryCopy.type === debugFiles_1.CustomRepoType.APP_STORE_CONNECT &&
                repositoryCopy.id === (appStoreConnectContext === null || appStoreConnectContext === void 0 ? void 0 : appStoreConnectContext.id)) {
                repositoryCopy.details = appStoreConnectContext;
            }
            return (<repository_1.default key={index} repository={repositoryCopy} onDelete={handleDeleteRepository} onEdit={handleEditRepository}/>);
        }))}
      </panels_1.PanelBody>
    </panels_1.Panel>);
}
exports.default = CustomRepositories;
const StyledMenuItem = (0, styled_1.default)(menuItem_1.default) `
  color: ${p => p.theme.textColor};
  font-size: ${p => p.theme.fontSizeMedium};
  font-weight: 400;
  text-transform: none;
  span {
    padding: 0;
  }
`;
//# sourceMappingURL=index.jsx.map