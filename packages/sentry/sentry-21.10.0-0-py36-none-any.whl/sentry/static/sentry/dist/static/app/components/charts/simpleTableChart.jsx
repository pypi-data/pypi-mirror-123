Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const panelTable_1 = (0, tslib_1.__importStar)(require("app/components/panels/panelTable"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const fieldRenderers_1 = require("app/utils/discover/fieldRenderers");
const fields_1 = require("app/utils/discover/fields");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const utils_1 = require("app/views/eventsV2/utils");
class SimpleTableChart extends react_1.Component {
    renderRow(index, row, tableMeta, columns) {
        const { location, organization } = this.props;
        return columns.map(column => {
            const fieldRenderer = (0, fieldRenderers_1.getFieldRenderer)(column.name, tableMeta);
            const rendered = fieldRenderer(row, { organization, location });
            return <TableCell key={`${index}:${column.name}`}>{rendered}</TableCell>;
        });
    }
    render() {
        const { className, loading, fields, metadata, data, title } = this.props;
        const meta = metadata !== null && metadata !== void 0 ? metadata : {};
        const columns = (0, utils_1.decodeColumnOrder)(fields.map(field => ({ field })));
        return (<react_1.Fragment>
        {title && <h4>{title}</h4>}
        <StyledPanelTable className={className} isLoading={loading} headers={columns.map((column, index) => {
                const align = (0, fields_1.fieldAlignment)(column.name, column.type, meta);
                return (<HeadCell key={index} align={align}>
                {column.name}
              </HeadCell>);
            })} isEmpty={!(data === null || data === void 0 ? void 0 : data.length)} disablePadding>
          {data === null || data === void 0 ? void 0 : data.map((row, index) => this.renderRow(index, row, meta, columns))}
        </StyledPanelTable>
      </react_1.Fragment>);
    }
}
const StyledPanelTable = (0, styled_1.default)(panelTable_1.default) `
  border-radius: 0;
  border-left: 0;
  border-right: 0;
  border-bottom: 0;

  margin: 0;
  ${ /* sc-selector */panelTable_1.PanelTableHeader} {
    height: min-content;
  }
`;
const HeadCell = (0, styled_1.default)('div') `
  ${(p) => (p.align ? `text-align: ${p.align};` : '')}
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(3)};
`;
const TableCell = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(3)};
`;
exports.default = (0, withOrganization_1.default)(SimpleTableChart);
//# sourceMappingURL=simpleTableChart.jsx.map