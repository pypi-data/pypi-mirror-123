Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const breadcrumbs_1 = require("app/types/breadcrumbs");
const default_1 = (0, tslib_1.__importDefault)(require("./default"));
const exception_1 = (0, tslib_1.__importDefault)(require("./exception"));
const http_1 = (0, tslib_1.__importDefault)(require("./http"));
const linkedEvent_1 = (0, tslib_1.__importDefault)(require("./linkedEvent"));
function Data({ breadcrumb, event, organization, searchTerm, route, router }) {
    var _a;
    const orgSlug = organization.slug;
    const linkedEvent = !!((_a = organization.features) === null || _a === void 0 ? void 0 : _a.includes('breadcrumb-linked-event')) &&
        breadcrumb.event_id ? (<linkedEvent_1.default orgSlug={orgSlug} eventId={breadcrumb.event_id} route={route} router={router}/>) : undefined;
    if (breadcrumb.type === breadcrumbs_1.BreadcrumbType.HTTP) {
        return (<http_1.default breadcrumb={breadcrumb} searchTerm={searchTerm} linkedEvent={linkedEvent}/>);
    }
    if (breadcrumb.type === breadcrumbs_1.BreadcrumbType.WARNING ||
        breadcrumb.type === breadcrumbs_1.BreadcrumbType.ERROR) {
        return (<exception_1.default breadcrumb={breadcrumb} searchTerm={searchTerm} linkedEvent={linkedEvent}/>);
    }
    return (<default_1.default event={event} orgSlug={orgSlug} breadcrumb={breadcrumb} searchTerm={searchTerm} linkedEvent={linkedEvent}/>);
}
exports.default = Data;
//# sourceMappingURL=index.jsx.map