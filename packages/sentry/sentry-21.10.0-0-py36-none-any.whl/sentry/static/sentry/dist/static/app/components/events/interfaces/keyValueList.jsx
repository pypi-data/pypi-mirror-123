Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const sortBy_1 = (0, tslib_1.__importDefault)(require("lodash/sortBy"));
const contextData_1 = (0, tslib_1.__importDefault)(require("app/components/contextData"));
const annotatedText_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotatedText"));
const utils_1 = require("app/utils");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const KeyValueList = ({ data, isContextData = false, isSorted = true, raw = false, longKeys = false, onClick, }) => {
    if (!(0, utils_1.defined)(data) || data.length === 0) {
        return null;
    }
    const getData = () => {
        if (isSorted) {
            return (0, sortBy_1.default)(data, [({ key }) => key.toLowerCase()]);
        }
        return data;
    };
    return (<table className="table key-value" onClick={onClick}>
      <tbody>
        {getData().map(({ key, subject, value = null, meta, subjectIcon, subjectDataTestId }) => {
            const dataValue = typeof value === 'object' && !React.isValidElement(value)
                ? JSON.stringify(value, null, 2)
                : value;
            let contentComponent = (<pre className="val-string">
                <annotatedText_1.default value={dataValue} meta={meta}/>
                {subjectIcon}
              </pre>);
            if (isContextData) {
                contentComponent = (<contextData_1.default data={!raw ? value : JSON.stringify(value)} meta={meta} withAnnotatedText>
                  {subjectIcon}
                </contextData_1.default>);
            }
            else if (typeof dataValue !== 'string' && React.isValidElement(dataValue)) {
                contentComponent = dataValue;
            }
            return (<tr key={key}>
                <TableSubject className="key" wide={longKeys}>
                  {subject}
                </TableSubject>
                <td className="val" data-test-id={subjectDataTestId}>
                  {contentComponent}
                </td>
              </tr>);
        })}
      </tbody>
    </table>);
};
const TableSubject = (0, styled_1.default)('td') `
  @media (min-width: ${theme_1.default.breakpoints[2]}) {
    max-width: ${p => (p.wide ? '620px !important' : 'none')};
  }
`;
KeyValueList.displayName = 'KeyValueList';
exports.default = KeyValueList;
//# sourceMappingURL=keyValueList.jsx.map