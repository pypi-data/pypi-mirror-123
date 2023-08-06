Object.defineProperty(exports, "__esModule", { value: true });
const locale_1 = require("app/locale");
function renderGroupingInfo(groupingInfo) {
    return Object.values(groupingInfo).map(renderGroupVariant).flat();
}
function renderGroupVariant(variant) {
    const title = [(0, locale_1.t)('Type: %s', variant.type)];
    if (variant.hash) {
        title.push((0, locale_1.t)('Hash: %s', variant.hash));
    }
    if (variant.description) {
        title.push((0, locale_1.t)('Description: %s', variant.description));
    }
    const rv = [title.join('\n')];
    if (variant.component) {
        rv.push(renderComponent(variant.component).join('\n'));
    }
    return rv;
}
function renderComponent(component) {
    if (!component.contributes) {
        return [];
    }
    const { name, id, hint } = component;
    const name_or_id = name || id;
    const title = name_or_id && hint ? `${name_or_id} (${hint})` : name_or_id;
    const rv = title ? [title] : [];
    if (component.values) {
        for (const value of component.values) {
            if (typeof value === 'string') {
                rv.push(`  ${value}`);
                continue;
            }
            for (const line of renderComponent(value)) {
                rv.push(`  ${line}`);
            }
        }
    }
    return rv;
}
exports.default = renderGroupingInfo;
//# sourceMappingURL=renderGroupingInfo.jsx.map