Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const capitalize_1 = (0, tslib_1.__importDefault)(require("lodash/capitalize"));
const styles_1 = require("app/components/charts/styles");
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const keyValueTable_1 = require("app/components/keyValueTable");
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const TagsTable = ({ event, query, generateUrl, title = (0, locale_1.t)('Tag Details') }) => {
    const eventWithMeta = (0, metaProxy_1.withMeta)(event);
    const tags = eventWithMeta.tags;
    const formatErrorKind = (kind) => {
        return (0, capitalize_1.default)(kind.replace(/_/g, ' '));
    };
    const getErrorMessage = (error) => {
        var _a;
        if (Array.isArray(error)) {
            if ((_a = error[1]) === null || _a === void 0 ? void 0 : _a.reason) {
                return formatErrorKind(error[1].reason);
            }
            else {
                return formatErrorKind(error[0]);
            }
        }
        return formatErrorKind(error);
    };
    const getTooltipTitle = (errors) => {
        return <TooltipTitle>{getErrorMessage(errors[0])}</TooltipTitle>;
    };
    return (<StyledTagsTable>
      <styles_1.SectionHeading>{title}</styles_1.SectionHeading>
      <keyValueTable_1.KeyValueTable>
        {tags.map(tag => {
            var _a, _b, _c;
            const tagInQuery = query.includes(`${tag.key}:`);
            const target = tagInQuery ? undefined : generateUrl(tag);
            const keyMetaData = (0, metaProxy_1.getMeta)(tag, 'key');
            const valueMetaData = (0, metaProxy_1.getMeta)(tag, 'value');
            const renderTagValue = () => {
                switch (tag.key) {
                    case 'release':
                        return <version_1.default version={tag.value} anchor={false} withPackage/>;
                    default:
                        return tag.value;
                }
            };
            return (<keyValueTable_1.KeyValueTableRow key={tag.key} keyName={((_a = keyMetaData === null || keyMetaData === void 0 ? void 0 : keyMetaData.err) === null || _a === void 0 ? void 0 : _a.length) ? (<tooltip_1.default title={getTooltipTitle(keyMetaData.err)}>
                    <i>{`<${(0, locale_1.t)('invalid')}>`}</i>
                  </tooltip_1.default>) : (tag.key)} value={((_b = valueMetaData === null || valueMetaData === void 0 ? void 0 : valueMetaData.err) === null || _b === void 0 ? void 0 : _b.length) ? (<tooltip_1.default title={getTooltipTitle(valueMetaData.err)}>
                    <i>{`<${(0, locale_1.t)('invalid')}>`}</i>
                  </tooltip_1.default>) : ((_c = keyMetaData === null || keyMetaData === void 0 ? void 0 : keyMetaData.err) === null || _c === void 0 ? void 0 : _c.length) ? (<span>{renderTagValue()}</span>) : tagInQuery ? (<tooltip_1.default title={(0, locale_1.t)('This tag is in the current filter conditions')}>
                    <span>{renderTagValue()}</span>
                  </tooltip_1.default>) : (<link_1.default to={target || ''}>{renderTagValue()}</link_1.default>)}/>);
        })}
      </keyValueTable_1.KeyValueTable>
    </StyledTagsTable>);
};
exports.default = TagsTable;
const StyledTagsTable = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(3)};
`;
const TooltipTitle = (0, styled_1.default)('div') `
  text-align: left;
`;
//# sourceMappingURL=tagsTable.jsx.map