Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const projects_1 = require("app/actionCreators/projects");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const BookmarkStar = ({ isBookmarked: isBookmarkedProp, className, organization, project, onToggle, }) => {
    const api = (0, useApi_1.default)();
    const isBookmarked = (0, utils_1.defined)(isBookmarkedProp)
        ? isBookmarkedProp
        : project.isBookmarked;
    const toggleProjectBookmark = (event) => {
        (0, projects_1.update)(api, {
            orgId: organization.slug,
            projectId: project.slug,
            data: { isBookmarked: !isBookmarked },
        }).catch(() => {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to toggle bookmark for %s', project.slug));
        });
        // needed to dismiss tooltip
        document.activeElement.blur();
        // prevent dropdowns from closing
        event.stopPropagation();
        if (onToggle) {
            onToggle(!isBookmarked);
        }
    };
    return (<Star isBookmarked={isBookmarked} isSolid={isBookmarked} onClick={toggleProjectBookmark} className={className}/>);
};
const Star = (0, styled_1.default)(icons_1.IconStar, { shouldForwardProp: p => p !== 'isBookmarked' }) `
  color: ${p => (p.isBookmarked ? p.theme.yellow300 : p.theme.gray200)};
  cursor: pointer;
`;
exports.default = BookmarkStar;
//# sourceMappingURL=bookmarkStar.jsx.map