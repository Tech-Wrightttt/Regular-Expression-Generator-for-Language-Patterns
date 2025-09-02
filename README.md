# Regular Expression Generator - Study Tool

## ⚠️ Important Disclaimer

**This is NOT a production-ready regular expression validator or generator.** This tool was created solely as a study aid for exam preparation and should not be used as a definitive reference for formal regular expression validation.

## 📖 Purpose

This application is a **study tool** designed to help understand:
- Basic regular expression concepts
- Common language patterns over the alphabet {a, b}
- How different patterns translate to regular expressions
- The limitations of simple regex generation approaches

## 🚫 Limitations and Known Issues

### 1. **Incomplete Implementations**
Several strategies are simplified or incomplete:
- **"Does not contain P"**: Only handles simple cases (aa, bb, ab, ba, single characters)
- **"Count divisible by N"**: Only works for very basic cases
- **Complex patterns**: Many edge cases are not handled properly

### 2. **Special Cases Not Handled**
The generator does NOT properly handle:
- Overlapping patterns in all scenarios
- Complex "does not contain" constraints
- Patterns with length constraints beyond simple cases
- All formal regular expression syntax rules

### 3. **Accuracy Issues**
- **False positives**: May generate expressions that accept invalid strings
- **False negatives**: May reject valid strings in some cases
- **Incomplete coverage**: Doesn't handle all possible language patterns

## 🎯 Intended Use Cases

Use this tool ONLY for:
1. **Study reference** when learning regular expressions
2. **Understanding basic patterns** and their corresponding regex
3. **Exam preparation** for introductory formal languages courses
4. **Getting ideas** about how certain patterns might be expressed

## ❌ What This Tool Should NOT Be Used For

Do NOT use this tool for:
- **Production code** - it's not reliable enough
- **Formal verification** - many expressions are simplified or incorrect
- **Grading assignments** - it may give incorrect answers
- **Definitive reference** - consult textbooks for accurate information

## 🔧 Work in Progress

This is very much a **work in progress** with these known issues:

### Patterns That Need Improvement:
1. **"Does not contain P"** - Only basic patterns supported
2. **"Count divisible by N"** - Very limited implementation
3. **Overlapping patterns** - Incomplete handling
4. **Complex constraints** - Many cases not covered

### Technical Debt:
- Some strategies use informal notation instead of proper formal syntax
- Error handling is minimal
- Test coverage is incomplete
- Performance could be improved for complex patterns

## 📚 Recommended Study Approach

1. **Use this tool to generate examples**
2. **Verify the results** with formal methods or textbooks
3. **Understand the limitations** of each approach
4. **Practice manually creating** regular expressions
5. **Test with various strings** to check if the regex works correctly

## 🎓 Exam Preparation Tips

While this tool can help you study, remember:
1. **Understand the concepts**, don't just memorize patterns
2. **Practice creating regex manually** - exams won't have this tool
3. **Learn the formal definitions** and syntax rules
4. **Be aware of the limitations** shown in this tool

## 🤝 Contributing

This is primarily a personal study project, but if you'd like to:
1. **Report bugs** or inaccuracies
2. **Suggest improvements** for study purposes
3. **Add better examples** for learning

Please feel free to open issues, but understand this is not intended to be a production-quality tool.

---

**Remember**: This tool is for **study purposes only** and should not be relied upon for accurate regular expression generation. Always verify with authoritative sources and formal methods.
