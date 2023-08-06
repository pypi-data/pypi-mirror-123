Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const diff_1 = require("diff");
const diffFnMap = {
    chars: diff_1.diffChars,
    words: diff_1.diffWords,
    lines: diff_1.diffLines,
};
const SplitDiff = ({ className, type = 'lines', base, target }) => {
    const diffFn = diffFnMap[type];
    const baseLines = base.split('\n');
    const targetLines = target.split('\n');
    const [largerArray] = baseLines.length > targetLines.length
        ? [baseLines, targetLines]
        : [targetLines, baseLines];
    const results = largerArray.map((_line, index) => diffFn(baseLines[index] || '', targetLines[index] || '', { newlineIsToken: true }));
    return (<SplitTable className={className}>
      <SplitBody>
        {results.map((line, j) => {
            const highlightAdded = line.find(result => result.added);
            const highlightRemoved = line.find(result => result.removed);
            return (<tr key={j}>
              <Cell isRemoved={highlightRemoved}>
                <Line>
                  {line
                    .filter(result => !result.added)
                    .map((result, i) => (<Word key={i} isRemoved={result.removed}>
                        {result.value}
                      </Word>))}
                </Line>
              </Cell>

              <Gap />

              <Cell isAdded={highlightAdded}>
                <Line>
                  {line
                    .filter(result => !result.removed)
                    .map((result, i) => (<Word key={i} isAdded={result.added}>
                        {result.value}
                      </Word>))}
                </Line>
              </Cell>
            </tr>);
        })}
      </SplitBody>
    </SplitTable>);
};
const SplitTable = (0, styled_1.default)('table') `
  table-layout: fixed;
  border-collapse: collapse;
  width: 100%;
`;
const SplitBody = (0, styled_1.default)('tbody') `
  font-family: ${p => p.theme.text.familyMono};
  font-size: ${p => p.theme.fontSizeSmall};
`;
const Cell = (0, styled_1.default)('td') `
  vertical-align: top;
  ${p => p.isRemoved && `background-color: ${p.theme.diff.removedRow}`};
  ${p => p.isAdded && `background-color: ${p.theme.diff.addedRow}`};
`;
const Gap = (0, styled_1.default)('td') `
  width: 20px;
`;
const Line = (0, styled_1.default)('div') `
  display: flex;
  flex-wrap: wrap;
`;
const Word = (0, styled_1.default)('span') `
  white-space: pre-wrap;
  word-break: break-all;
  ${p => p.isRemoved && `background-color: ${p.theme.diff.removed}`};
  ${p => p.isAdded && `background-color: ${p.theme.diff.added}`};
`;
exports.default = SplitDiff;
//# sourceMappingURL=splitDiff.jsx.map