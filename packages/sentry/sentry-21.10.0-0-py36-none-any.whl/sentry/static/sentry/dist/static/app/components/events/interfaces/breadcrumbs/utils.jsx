Object.defineProperty(exports, "__esModule", { value: true });
exports.transformCrumbs = void 0;
const locale_1 = require("app/locale");
const breadcrumbs_1 = require("app/types/breadcrumbs");
const utils_1 = require("app/utils");
function convertCrumbType(breadcrumb) {
    if (breadcrumb.type === breadcrumbs_1.BreadcrumbType.EXCEPTION) {
        return Object.assign(Object.assign({}, breadcrumb), { type: breadcrumbs_1.BreadcrumbType.ERROR });
    }
    // special case for 'ui.' and `sentry.` category breadcrumbs
    // TODO: find a better way to customize UI around non-schema data
    if (breadcrumb.type === breadcrumbs_1.BreadcrumbType.DEFAULT && (0, utils_1.defined)(breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.category)) {
        const [category, subcategory] = breadcrumb.category.split('.');
        if (category === 'ui') {
            return Object.assign(Object.assign({}, breadcrumb), { type: breadcrumbs_1.BreadcrumbType.UI });
        }
        if (category === 'console') {
            return Object.assign(Object.assign({}, breadcrumb), { type: breadcrumbs_1.BreadcrumbType.DEBUG });
        }
        if (category === 'navigation') {
            return Object.assign(Object.assign({}, breadcrumb), { type: breadcrumbs_1.BreadcrumbType.NAVIGATION });
        }
        if (category === 'sentry' &&
            (subcategory === 'transaction' || subcategory === 'event')) {
            return Object.assign(Object.assign({}, breadcrumb), { type: breadcrumbs_1.BreadcrumbType.TRANSACTION });
        }
    }
    if (!Object.values(breadcrumbs_1.BreadcrumbType).includes(breadcrumb.type)) {
        return Object.assign(Object.assign({}, breadcrumb), { type: breadcrumbs_1.BreadcrumbType.DEFAULT });
    }
    return breadcrumb;
}
function getCrumbDescriptionAndColor(type) {
    switch (type) {
        case breadcrumbs_1.BreadcrumbType.USER:
        case breadcrumbs_1.BreadcrumbType.UI:
            return {
                color: 'purple300',
                description: (0, locale_1.t)('User Action'),
            };
        case breadcrumbs_1.BreadcrumbType.NAVIGATION:
            return {
                color: 'green300',
                description: (0, locale_1.t)('Navigation'),
            };
        case breadcrumbs_1.BreadcrumbType.DEBUG:
            return {
                color: 'purple300',
                description: (0, locale_1.t)('Debug'),
            };
        case breadcrumbs_1.BreadcrumbType.INFO:
            return {
                color: 'blue300',
                description: (0, locale_1.t)('Info'),
            };
        case breadcrumbs_1.BreadcrumbType.ERROR:
            return {
                color: 'red300',
                description: (0, locale_1.t)('Error'),
            };
        case breadcrumbs_1.BreadcrumbType.HTTP:
            return {
                color: 'green300',
                description: (0, locale_1.t)('HTTP request'),
            };
        case breadcrumbs_1.BreadcrumbType.WARNING:
            return {
                color: 'orange400',
                description: (0, locale_1.t)('Warning'),
            };
        case breadcrumbs_1.BreadcrumbType.QUERY:
            return {
                color: 'blue300',
                description: (0, locale_1.t)('Query'),
            };
        case breadcrumbs_1.BreadcrumbType.SYSTEM:
            return {
                color: 'pink300',
                description: (0, locale_1.t)('System'),
            };
        case breadcrumbs_1.BreadcrumbType.SESSION:
            return {
                color: 'orange300',
                description: (0, locale_1.t)('Session'),
            };
        case breadcrumbs_1.BreadcrumbType.TRANSACTION:
            return {
                color: 'pink300',
                description: (0, locale_1.t)('Transaction'),
            };
        default:
            return {
                color: 'gray300',
                description: (0, locale_1.t)('Default'),
            };
    }
}
function transformCrumbs(breadcrumbs) {
    return breadcrumbs.map((breadcrumb, index) => {
        var _a;
        const convertedCrumbType = convertCrumbType(breadcrumb);
        const { color, description } = getCrumbDescriptionAndColor(convertedCrumbType.type);
        return Object.assign(Object.assign({}, convertedCrumbType), { id: index, color,
            description, level: (_a = convertedCrumbType.level) !== null && _a !== void 0 ? _a : breadcrumbs_1.BreadcrumbLevelType.UNDEFINED });
    });
}
exports.transformCrumbs = transformCrumbs;
//# sourceMappingURL=utils.jsx.map