Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const integration_docs_platforms_1 = (0, tslib_1.__importDefault)(require("integration-docs-platforms"));
const locale_1 = require("app/locale");
const platformCategories_1 = require("./platformCategories");
const otherPlatform = {
    integrations: [
        {
            link: 'https://docs.sentry.io/platforms/',
            type: 'language',
            id: 'other',
            name: (0, locale_1.t)('Other'),
        },
    ],
    id: 'other',
    name: (0, locale_1.t)('Other'),
};
exports.default = [].concat([], ...[...integration_docs_platforms_1.default.platforms, otherPlatform].map(platform => platform.integrations
    .map(i => (Object.assign(Object.assign({}, i), { language: platform.id })))
    // filter out any tracing platforms; as they're not meant to be used as a platform for
    // the project creation flow
    .filter(integration => !platformCategories_1.tracing.includes(integration.id))));
//# sourceMappingURL=platforms.jsx.map