Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const globalSelectionLink_1 = (0, tslib_1.__importDefault)(require("app/components/globalSelectionLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const icons_1 = require("app/icons");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const breadcrumbDropdown_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/breadcrumbDropdown"));
const BreadcrumbList = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  padding: ${(0, space_1.default)(1)} 0;
`;
function isCrumbDropdown(crumb) {
    return crumb.items !== undefined;
}
/**
 * Page breadcrumbs used for navigation, not to be confused with sentry's event breadcrumbs
 */
const Breadcrumbs = (_a) => {
    var { crumbs, linkLastItem = false } = _a, props = (0, tslib_1.__rest)(_a, ["crumbs", "linkLastItem"]);
    if (crumbs.length === 0) {
        return null;
    }
    if (!linkLastItem) {
        const lastCrumb = crumbs[crumbs.length - 1];
        if (!isCrumbDropdown(lastCrumb)) {
            lastCrumb.to = null;
        }
    }
    return (<BreadcrumbList {...props}>
      {crumbs.map((crumb, index) => {
            if (isCrumbDropdown(crumb)) {
                const { label } = crumb, crumbProps = (0, tslib_1.__rest)(crumb, ["label"]);
                return (<breadcrumbDropdown_1.default key={index} isLast={index >= crumbs.length - 1} route={{}} name={label} {...crumbProps}/>);
            }
            else {
                const { label, to, preserveGlobalSelection, key } = crumb;
                const labelKey = typeof label === 'string' ? label : '';
                const mapKey = (key !== null && key !== void 0 ? key : typeof to === 'string') ? `${labelKey}${to}` : `${labelKey}${index}`;
                return (<React.Fragment key={mapKey}>
              {to ? (<BreadcrumbLink to={to} preserveGlobalSelection={preserveGlobalSelection}>
                  {label}
                </BreadcrumbLink>) : (<BreadcrumbItem>{label}</BreadcrumbItem>)}

              {index < crumbs.length - 1 && (<BreadcrumbDividerIcon size="xs" direction="right"/>)}
            </React.Fragment>);
            }
        })}
    </BreadcrumbList>);
};
const getBreadcrumbListItemStyles = (p) => `
  color: ${p.theme.gray300};
  ${overflowEllipsis_1.default};
  width: auto;

  &:last-child {
    color: ${p.theme.textColor};
  }
`;
const BreadcrumbLink = (0, styled_1.default)((_a) => {
    var { preserveGlobalSelection, to } = _a, props = (0, tslib_1.__rest)(_a, ["preserveGlobalSelection", "to"]);
    return preserveGlobalSelection ? (<globalSelectionLink_1.default to={to} {...props}/>) : (<link_1.default to={to} {...props}/>);
}) `
  ${getBreadcrumbListItemStyles}

  &:hover,
  &:active {
    color: ${p => p.theme.subText};
  }
`;
const BreadcrumbItem = (0, styled_1.default)('span') `
  ${getBreadcrumbListItemStyles}
  max-width: 400px;
`;
const BreadcrumbDividerIcon = (0, styled_1.default)(icons_1.IconChevron) `
  color: ${p => p.theme.gray300};
  margin: 0 ${(0, space_1.default)(1)};
  flex-shrink: 0;
`;
exports.default = Breadcrumbs;
//# sourceMappingURL=breadcrumbs.jsx.map