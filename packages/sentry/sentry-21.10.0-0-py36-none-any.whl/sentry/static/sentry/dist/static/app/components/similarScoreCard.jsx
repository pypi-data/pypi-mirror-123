Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const scoreComponents = {
    'exception:message:character-shingles': (0, locale_1.t)('Exception Message'),
    'exception:stacktrace:pairs': (0, locale_1.t)('Stack Trace Frames'),
    'exception:stacktrace:application-chunks': (0, locale_1.t)('In-App Frames'),
    'message:message:character-shingles': (0, locale_1.t)('Log Message'),
    // v2
    'similarity:*:type:character-5-shingle': (0, locale_1.t)('Exception Type'),
    'similarity:*:value:character-5-shingle': (0, locale_1.t)('Exception Message'),
    'similarity:*:stacktrace:frames-pairs': (0, locale_1.t)('Stack Trace Frames'),
    'similarity:*:message:character-5-shingle': (0, locale_1.t)('Log Message'),
};
const SimilarScoreCard = ({ scoreList = [] }) => {
    if (scoreList.length === 0) {
        return null;
    }
    let sumOtherScores = 0;
    let numOtherScores = 0;
    return (<react_1.Fragment>
      {scoreList.map(([key, score]) => {
            const title = scoreComponents[key.replace(/similarity:\d\d\d\d-\d\d-\d\d/, 'similarity:*')];
            if (!title) {
                if (score !== null) {
                    sumOtherScores += score;
                    numOtherScores += 1;
                }
                return null;
            }
            return (<Wrapper key={key}>
            <div>{title}</div>
            <Score score={score === null ? score : Math.round(score * 4)}/>
          </Wrapper>);
        })}

      {numOtherScores > 0 && sumOtherScores > 0 && (<Wrapper>
          <div>{(0, locale_1.t)('Other')}</div>
          <Score score={Math.round((sumOtherScores * 4) / numOtherScores)}/>
        </Wrapper>)}
    </react_1.Fragment>);
};
const Wrapper = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  margin: ${(0, space_1.default)(0.25)} 0;
`;
const Score = (0, styled_1.default)('div') `
  height: 16px;
  width: 48px;
  border-radius: 2px;
  background-color: ${p => p.score === null ? p.theme.similarity.empty : p.theme.similarity.colors[p.score]};
`;
exports.default = SimilarScoreCard;
//# sourceMappingURL=similarScoreCard.jsx.map