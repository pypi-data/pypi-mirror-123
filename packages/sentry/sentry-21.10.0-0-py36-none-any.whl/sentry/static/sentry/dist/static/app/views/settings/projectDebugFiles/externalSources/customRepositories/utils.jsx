Object.defineProperty(exports, "__esModule", { value: true });
exports.expandKeys = exports.getRequestMessages = exports.dropDownItems = exports.customRepoTypeLabel = void 0;
const tslib_1 = require("tslib");
const forEach_1 = (0, tslib_1.__importDefault)(require("lodash/forEach"));
const set_1 = (0, tslib_1.__importDefault)(require("lodash/set"));
const locale_1 = require("app/locale");
const debugFiles_1 = require("app/types/debugFiles");
exports.customRepoTypeLabel = {
    [debugFiles_1.CustomRepoType.APP_STORE_CONNECT]: 'App Store Connect',
    [debugFiles_1.CustomRepoType.HTTP]: 'SymbolServer (HTTP)',
    [debugFiles_1.CustomRepoType.S3]: 'Amazon S3',
    [debugFiles_1.CustomRepoType.GCS]: 'Google Cloud Storage',
};
exports.dropDownItems = [
    {
        value: debugFiles_1.CustomRepoType.S3,
        label: exports.customRepoTypeLabel[debugFiles_1.CustomRepoType.S3],
        searchKey: (0, locale_1.t)('aws amazon s3 bucket'),
    },
    {
        value: debugFiles_1.CustomRepoType.GCS,
        label: exports.customRepoTypeLabel[debugFiles_1.CustomRepoType.GCS],
        searchKey: (0, locale_1.t)('gcs google cloud storage bucket'),
    },
    {
        value: debugFiles_1.CustomRepoType.HTTP,
        label: exports.customRepoTypeLabel[debugFiles_1.CustomRepoType.HTTP],
        searchKey: (0, locale_1.t)('http symbol server ssqp symstore symsrv'),
    },
];
function getRequestMessages(updatedRepositoriesQuantity, repositoriesQuantity) {
    if (updatedRepositoriesQuantity > repositoriesQuantity) {
        return {
            successMessage: (0, locale_1.t)('Successfully added custom repository'),
            errorMessage: (0, locale_1.t)('An error occurred while adding a new custom repository'),
        };
    }
    if (updatedRepositoriesQuantity < repositoriesQuantity) {
        return {
            successMessage: (0, locale_1.t)('Successfully removed custom repository'),
            errorMessage: (0, locale_1.t)('An error occurred while removing the custom repository'),
        };
    }
    return {
        successMessage: (0, locale_1.t)('Successfully updated custom repository'),
        errorMessage: (0, locale_1.t)('An error occurred while updating the custom repository'),
    };
}
exports.getRequestMessages = getRequestMessages;
function expandKeys(obj) {
    const result = {};
    (0, forEach_1.default)(obj, (value, key) => {
        (0, set_1.default)(result, key.split('.'), value);
    });
    return result;
}
exports.expandKeys = expandKeys;
//# sourceMappingURL=utils.jsx.map