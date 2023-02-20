#include <iostream>
#include <fstream>
#include <bits/stdc++.h>
#include <cstdlib>
#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "llvm/IR/InstrTypes.h"
#include <string>
#include "llvm/IR/Value.h"
#include "llvm/IR/CFG.h"
#include "llvm/IR/Instruction.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/Constants.h"
#include "llvm/Support/Casting.h"
#include "llvm/IR/User.h"
#include "llvm/IR/Type.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Metadata.h"
#include "llvm/IR/Constant.h"
#include "clang/AST/Type.h"
#include "interPro.h"


using namespace std;
using namespace llvm;
//using namespace StaticAnalysis;
StringRef configVar;
int numOfValue = 0;

//reading file name
char *Filename_file = "file_name";
std::ifstream infile_file(Filename_file);
std::string line_file;

std::error_code EC;
enum sys::fs::OpenFlags F_None;
//std::string name = "encrypt";
//StringRef filename(name);
//StringRef filename(line_file);
//llvm::raw_fd_ostream file(filename, EC, F_None);


Value* maxValue;
Value* minValue;
int mapping = 0;
std::map<StringRef, Value *> var2sbMap;
Value *var;

std::string name1 = "sb_name";
StringRef filename1(name1);
//llvm::raw_fd_ostream file1(filename1, EC, F_None);

//std::string line;
//std::ifstream myfile( "sb_name", std::ifstream::in );

string func_name = "PRS";
//string func_name = "validate_blocksize";
namespace StaticAnalysis{
	int depth = 0;
	std::map<Value *, bool> taintMap;
	//std::queue<Instruction *> taintInst;
	//std::queue<std::pair<Instruction *, unsigned> > taintInst;
	//std::deque<std::pair<Instruction *, unsigned> > dq;
	std::queue<std::pair<Instruction *, Instruction *> > taintInst;
	std::deque<std::pair<Instruction *, Instruction *> > dq;
	//std::deque<Instruction *> dq;
        struct InterProPass : public ModulePass {
		static char ID;
		//string func_name = "PRS";
		
		InterProPass() : ModulePass(ID) {}

		//declares all the functions of the pass
		virtual bool runOnModule(Module& m);
	};

/*
class Analysis
{
public:
	Analysis(Function *func);

};

Analysis::Analysis(Function *func)
{
	errs() << "inside the class constructor: " << func->getName() << "\n";
	for (Function::iterator b = func->begin(), be = func->end(); b != be; ++b) {
		BasicBlock& BB = *b;
		for (auto& I : BB) {
			errs() << I << "\n";
		}
	}

}
*/

void TaintAnalysis::Analysis(Function *func)
{
	//errs() << "inside the class constructor: " << func->getName() << "\n";
	for (Function::iterator b = func->begin(), be = func->end(); b != be; ++b) {
                BasicBlock& BB = *b;
                for (auto& I : BB) {
                        errs() << "" << "\n";
			//TaintAnalysis::functionProcess(*func, NULL);
                }
        }
}

//Analyzes store instructions to taint relevant variables
void TaintAnalysis::taintStore(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1)
{
          Value *op1 = I.getOperand(0);
          Value *op2 = I.getOperand(1);
          Instruction *i = dyn_cast<Instruction>(&I);
	  //MDNode* debug = I.getMetadata("dbg");
	  if(taintMap.find(op1) != taintMap.end())
          {
                  taintInst.push({&I, line_no1});
		  //errs() << I << "\n";
		  //taintInst.push(make_pair( &I, debug1));
		  //errs() << taintInst.size() << "\n";
                  StringRef name = op2->getName();
                  //errs() << name << "\n";
                  if (!((name == "inode_ratio") || (name == "inode_size") || (name == "blocksize") || (name == "cluster_size") || (name == "inode_size")
                                  || (name == "num_inodes") || (name == "fs_blocks_count") || (name == "r_opt") || (name == "flex_bg_size") || (name == "reserved_ratio") || (name == "cluster_size")
                                  || (name == "fs_type") || (name == "fs_types") || (name == "s_blocks_count") || (name == "s_log_block_size") || (name == "s_blocks_per_group") || (name == "s_inodes_count")
                                  || (name == "new_size") || (name == "journal_location") || (name == "cflag") || (name == "creator_os") || (name == "direct_io") || (name == "errors_behavior") || (name == "force") || (name == "fs_uuid") || (name == "journal_size") || (name == "mount_dir") || (name == "quiet") ||  (name == "src_root_dir") || (name == "super_only") || (name == "undo_file") || (name == "volume_label") || (name == "verbose") || (name == "desc-size") || (name == "hash_seed") || (name == "offset") || (name == "mmp_update_interval") || (name == "no_copy_xattrs") || (name == "num_backup_sb") || (name == "packed_meta_blocks") || (name == "stride") || (name == "stripe-width") || (name == "resize") || (name == "test_fs") || (name == "lazy_itable_init") || (name == "assume_storage_prezeroed") || (name == "discard") || (name == "quotatype_bits") || (name == "encoding") || (name == "encoding_flags") || (name == "orphan_file_blocks") || (name == "journal_device") || (name == "retval") || (name == "retval1") || (name == "tmp"))) {
//                  if (!((name == "force") || (name == "flush") || (name == "force_min_size") || (name == "print_min_size") || (name == "use_stride") || (name == "undo_file") || (name == "new_size") || (name == "retval") || (name == "retval1") || (name == "tmp") || (name == "checkit") )) { 
		  taintMap.insert(std::pair<Value *, bool>(op2, 1));
                  }
	  }

	  if(taintMap.find(op2) != taintMap.end())
          {
                //errs() << I << "\n";
		  taintInst.push({&I, line_no1});
	  }
}

//Analyzes Binary instructions to taint relevant variables
void TaintAnalysis::taintBinaryOperator(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1)
{
	//errs() << I << "\n";
        Value *op1 = I.getOperand(0);
        Value *op2 = I.getOperand(1);
        Value *op3 = dyn_cast<Value>(&I);
        Instruction *i = dyn_cast<Instruction>(&I);
	
        if(taintMap.find(op1) != taintMap.end())
        {
                taintMap.insert(std::pair<Value *, bool>(op3, 1));
                taintInst.push({i, line_no1});
        }
        else if (taintMap.find(op2) != taintMap.end())
        {
                taintMap.insert(std::pair<Value *, bool>(op3, 1));
                taintInst.push({i, line_no1});
        }
}

//Analyzes Load instructions to taint relevant variables
void TaintAnalysis::taintLoad(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1)
{
    Value *op1 = I.getOperand(0);
    Value *op2 = dyn_cast<Value>(&I);
    Instruction *i = dyn_cast<Instruction>(&I);
	//MDNode* debug = I.getMetadata("dbg");
    if(taintMap.find(op1) != taintMap.end())
    {
        taintMap.insert(std::pair<Value *, bool>(op2, 1));
	//errs() << I <<"\n";
	//errs() << *op1 <<"\n";
        taintInst.push({i, line_no1});
	//taintInst.push(make_pair(i, NULL));
	/*errs() << taintInst.size() << "\n";
	while (!taintInst.empty()) {
                std::pair <llvm::Instruction* , llvm::MDNode*> test1 = taintInst.front();
                errs() << *test1.first << ":" << test1.second << "\n";
		taintInst.pop();
	}*/
    }
}

//Analyzes Icmp instructions to taint relevant variables
void TaintAnalysis::taintIcmp(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1)
{
        Instruction *i = dyn_cast<Instruction>(&I);
        Value *v1 = dyn_cast<Instruction>(&I);
        for(unsigned j=0;j<I.getNumOperands(); j++) {
            Value* currOp = I.getOperand(j);
            if(taintMap.find(currOp) != taintMap.end())
            {
		    //errs() << "value found in map" << "\n";
                taintInst.push({i, line_no1});
                taintMap.insert(std::pair<Value *, bool>(v1, 1));
            }
        }
}

//Analyzes Fcmp instructions to taint relevant variables
void TaintAnalysis::taintFcmp(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1)
{
        Instruction *i = dyn_cast<Instruction>(&I);
        Value *v1 = dyn_cast<Instruction>(&I);
        Value *op2 = I.getOperand(0);

            if(taintMap.find(op2) != taintMap.end())
            {
                taintInst.push({&I, line_no1});
               // taintMap.insert(std::pair<Value *, bool>(v1, 1));
            }

}

//Analyzes GetElementPtr instructions to taint relevant variables
void TaintAnalysis::taintGetElementPtr(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1)
{
        Instruction *i = dyn_cast<Instruction>(&I);
        Value *op1 = dyn_cast<Instruction>(&I);
        for(unsigned j=0;j<I.getNumOperands(); j++) {
            Value* currOp = I.getOperand(j);
            if(taintMap.find(currOp) != taintMap.end())
            {
                taintMap.insert(std::pair<Value *, bool>(op1, 1));
                taintInst.push({&I, line_no1});
            }
        }
}

//Analyzes Select instructions to taint relevant variables
void TaintAnalysis::taintSelect(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1)
{
        Instruction *i = dyn_cast<Instruction>(&I);
        SelectInst *i1 =dyn_cast<SelectInst>(&I);
        Value* v1 = i1->getOperand(0);
        if(taintMap.find(v1) != taintMap.end())
        {
                //errs() << "select instruction :" << (*v1) <<"\n";
                taintInst.push({&I, line_no1});
        }
}

//Analyzes Conversion instructions to taint relevant variables
void TaintAnalysis::taintConversion(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1)
{
        Value *op1 = I.getOperand(0);
        Value *op2 = dyn_cast<Value>(&I);

        if(taintMap.find(op1) != taintMap.end())
        {
                taintMap.insert(std::pair<Value *, bool>(op2, 1));
                taintInst.push({&I, line_no1});
        }
}

//Analyzes Branch instructions to taint relevant variables
void TaintAnalysis::taintBr(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1)
{
        unsigned int a = I.getNumOperands();
        if (a > 1)
        {
                Value *op1 = I.getOperand(0);
                if(taintMap.find(op1) != taintMap.end())
                {

                        ICmpInst* Cinst = dyn_cast<ICmpInst>(&*op1);
                        BranchInst* Binst = dyn_cast<BranchInst>(&I);
                        taintInst.push({&I, line_no1});
                        BasicBlock *Succ1 = Binst->getSuccessor(0);
                        BasicBlock *Succ2 = Binst->getSuccessor(1);
                        StringRef name1 = Succ1->getName();
                        StringRef name2 = Succ2->getName();
                        string s1 = "end";

                        //When the branch label doesn't end with "end" then taint the first instruction of that branch
                        if (name1.find(s1) == string::npos){
                                Instruction* I3 = dyn_cast<Instruction>(&*(Succ1->begin()));
                                taintInst.push({I3, line_no1});
                                Value* v2 = dyn_cast<Value>(I3);
                                taintMap.insert(std::pair<Value *, bool>(v2, 1));
                        }
                        else if (name2.find(s1) == string::npos)
                        {
                                BasicBlock *Succ1 = Binst->getSuccessor(1);
                                Instruction* I4 = dyn_cast<Instruction>(&*(Succ1->begin()));
                                taintInst.push({I4, line_no1});
                                Value* v3  = dyn_cast<Value>(I4);
                                taintMap.insert(std::pair<Value *, bool>(v3, 1));
                        }
                }
        }
}

//Analyzes Phi instructions to taint relevant variables
void TaintAnalysis::taintPhi(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1)
{
        Value *op1 = I.getOperand(0);
        Value *op2 = I.getOperand(1);
        Value *op3 = dyn_cast<Value>(&I);
        if(taintMap.find(op1) != taintMap.end())
        {
                taintMap.insert(std::pair<Value *, bool>(op3, 1));
                taintInst.push({&I, line_no1});
        }
        else if (taintMap.find(op2) != taintMap.end())
        {
                taintMap.insert(std::pair<Value *, bool>(op3, 1));
                taintInst.push({&I, line_no1});
        }
}

//Analyzes Call instructions to taint relevant variables
void TaintAnalysis::taintCallInst(Instruction &I, std::map<Value *, bool> &taintMap, Instruction *line_no1)
{
	//const DebugLoc &D = I.getDebugLoc ();
	//unsigned line_no = D.getLine();
	Value* op1 = dyn_cast<Value>(&I);
        CallInst* call = dyn_cast<CallInst>(&I);
	 //errs() << I << "\n";
	//Function *F = call->getCalledFunction();
	/*
	if (call->getCalledFunction() == NULL){
        	Function *F = dyn_cast<Function>(call->getCalledOperand()->stripPointerCasts());
		if (F->isVarArg () == 0){
			errs() << "this is nullptr" << "\n";}
		errs() << "-----------------" << "\n";
	       	unsigned int V2 = F->arg_size();
		 errs() << "arg size: " << V2 << "\n";
	

	//parsing functions when at least one arguments of the function is tainted
        	for(int i = 0; i < V2; i++)
        	{
                	Value* V1 = call->getArgOperand(i);
			errs() << "getArgOperand: " << *V1 << "\n";
                	if(taintMap.find(V1) != taintMap.end())
                	{
				errs() << "found, yes!! " << "\n";
                        	taintMap.insert(std::pair<Value *, bool>(op1, 1));
                        	taintInst.push({&I, NULL});
				if (!F->hasExternalLinkage()){
        		      		if (!F->isIntrinsic ()){
						TaintAnalysis::propogateTaintToArguments(i, I, F);
						TaintAnalysis::functionProcess(*F, &I);
			      		}
				}
                	}
			errs() << "didn't find " << "\n";
        	}
		errs() << "didn't find 2" << "\n";
		if (!F->hasExternalLinkage()){
			errs() << "ready to go to process function 1" << "\n";
                         if (!F->isIntrinsic ()){
				 errs() << "ready to go to process function " << "\n";
				 TaintAnalysis::functionProcess(*F, &I);
			 }
		}
		errs() << "didn't find 3" << "\n";
	}
	*/
	if (call->getCalledFunction() != NULL)
	{
		Function *F = call->getCalledFunction();
		 unsigned int V2 = F->arg_size();
		for(int i = 0; i < V2; i++)
        	{
                Value* V1 = call->getArgOperand(i);
                if(taintMap.find(V1) != taintMap.end())
                {
                        taintMap.insert(std::pair<Value *, bool>(op1, 1));
                        taintInst.push({&I, NULL});
			if (!F->hasExternalLinkage()){
				if (!F->isIntrinsic ()){
                        		TaintAnalysis::propogateTaintToArguments(i, I, F);
                        		TaintAnalysis::functionProcess(*F, &I);
				}
			}
                }
        	}

		//Parsing function when arguments are not tainted
		// if (!F->hasExternalLinkage() || F->isDSOLocal()){
		if (!F->hasExternalLinkage()){
				 //errs() << F->getName() << ":" << I << "\n";
				TaintAnalysis::functionProcess(*F, &I);
			
		}
	}
/*	
	//Parsing function when arguments are not tainted
	
	if (call->getCalledFunction() != NULL){
	       	if ((call->getCalledFunction()->getName() == "PRS")){
		//if ((call->getCalledFunction()->getName() == "e2fsck_pass1")){ 
				//|| (call->getCalledFunction()->getName() == "e2fsck_pass1_check_symlink") || (call->getCalledFunction()->getName() == "e2fsck_pass1_check_device_inode") || (call->getCalledFunction()->getName() == "e2fsck_pass2") || (call->getCalledFunction()->getName() == "e2fsck_pass3") || (call->getCalledFunction()->getName() == "e2fsck_pass4") || (call->getCalledFunction()->getName() == "e2fsck_pass5") || (call->getCalledFunction()->getName() == "e2fsck_pass1e")){
	//if (call->getCalledFunction() != NULL && (call->getCalledFunction()->getName() == "resize_fs")){
	//if (F->getName() == "resize_fs"){
		errs() << "PRS found" << "\n";
		TaintAnalysis::functionProcess(*(call->getCalledFunction()), &I);
}
}
*/
}

void TaintAnalysis::propogateTaintToArguments(int taintedArgNo, Instruction &I, Function *F)
{
	//int taintedArgNo;
	//assert(taintedArgNo > 0);
	CallInst* call = dyn_cast<CallInst>(&I);

	//errs() << "Propagating Taint To Arguments.\n";
	//Function *func = call->getCalledFunction();
	//unsigned int V2 = func->arg_size();
	unsigned int V2 = F->arg_size();
	if (V2 > 0){
		Value *currArg = call->getArgOperand(taintedArgNo);
		Argument* i = F->getArg(taintedArgNo);
		taintMap.insert(std::pair<Value *, bool>(i, 1));
	}
}

//Prints the tainted instructions on the std output and also writes them on a file named "module"
void TaintAnalysis::printInst(std::queue<std::pair<Instruction *, Instruction *> > taintInst, Module& m)
{
        //std::error_code EC;
        //enum sys::fs::OpenFlags F_None;
        //std::string name = "module";
	StringRef filename(line_file);
        llvm::raw_fd_ostream file(filename, EC, F_None);

        errs() <<"The size of the queue is: " << taintInst.size() << "\n";
        int size = taintInst.size();

        errs() <<"The tainted Instructions are: " << "\n";
        int i = 0;
	while (!taintInst.empty()) {
                std::pair <llvm::Instruction* , Instruction *> test1 = taintInst.front();
                dq.push_back(test1);
		if (test1.second == NULL)
                	file << *test1.first << ":" << test1.second << "\n";
		else
			file << *test1.first << ":" << *test1.second << "\n";

		unsigned opcode = test1.first->getOpcode();
		if (opcode == llvm::Instruction::Call){
			CallInst* call = dyn_cast<CallInst>(test1.first);
			Function *F = call->getCalledFunction();
			if (F != NULL){
				StringRef name = F->getName();
				//if (name == "stderr" || name == "fprintf"){ //(for xfs)
				if (name == "fprintf" || name == "com_err"){ //(for ext4)
					errs() << "found stderr" << "\n";
					//errs() << *test1.first << "\n";
					dataRange(test1.first, m, &file);
				}
			}
		}

                taintInst.pop();
		//file << test1 << "\n";
         }
        file.close();
	/*
	for(Instruction* n : dq.front().first) {	
        //while(dq.front().first) {
	//for (auto it = dq.begin(); it != dq.end(); ++it){
                //unsigned opcode = n->getOpcode();
		//if (numOfValue <2){
		unsigned opcode = n->getOpcode();
                if (opcode == llvm::Instruction::Call)
                {
                        //CallInst* call = dyn_cast<CallInst>(n);
			CallInst* call = dyn_cast<CallInst>(n);
                        Function *F = call->getCalledFunction();
                        if (F != NULL){
                                StringRef name = F->getName();
                                if (name == "fprintf" || name == "com_err")
                                {
                                        errs() << *n << "\n";
                                        //dataRange(n, m);
					dataRange(n, m);
                                }


                        }
                }
		//dq.pop_front();	
		//}*/
        //}
        //file.close();

}


//Gets the data range of parameters
void TaintAnalysis::dataRange(Instruction *Inst, Module& m, raw_fd_ostream* stream)
{	if (numOfValue < 2){
  	for(auto& F : m){
       //         if (F.getName() == "validate_sectorsize" ){
                        //errs() << "Hello from: data range : "<< F.getName() << "\n";
                        for (auto& B : F) {
                                for (auto& I : B) {
                                        if (&I == Inst){
                                                errs() << "found fprintf in main file" << "\n";
                                                for (BasicBlock* Pred : predecessors(&B))
                                                {
                                                        BasicBlock& predecessor = *Pred;
                                                        for (auto& i : predecessor){
                                                                errs() << i << "\n";
                                                                unsigned opcode = i.getOpcode();
                                                                errs() << opcode << "\n";
                                                                if (opcode == llvm::Instruction::ICmp || opcode == llvm::Instruction::FCmp)
                                                                {
                                                                        CmpInst* inst = dyn_cast<CmpInst>(&i);
                                                                        Value* op1 = i.getOperand(1);
                                                                        StringRef S = op1->getName();
                                                                        if (S.empty())
                                                                        {
                                                                                //if (numOfValue < 2)
                                                                                //{
                                                                                        llvm::CmpInst::Predicate p = inst->getPredicate();
                                                                                        if (inst->getPredicate() == 34 || inst->getPredicate() == 38)
                                                                                        {
                                                                                //errs() << "Range is <= " << *i.getOperand(1)  << "\n";
                                                                                                Value* maxValue = i.getOperand(1);
                                                                                                errs() << "Max value is: " << *maxValue << "\n";
                                                                                                *stream << "Max value = " << *maxValue << "\n";
                                                                                                numOfValue = numOfValue + 1;
                                                                                                //errs() << numOfValue << "\n";
                                                                                        }
                                                                                        else if (inst->getPredicate() == 35 || inst->getPredicate() == 39 || inst->getPredicate() == 2)
                                                                                        {
                                                                                                Value* maxValue = i.getOperand(1);
                                                                                                errs() << "Max value is < " << *maxValue  << "\n";
                                                                                                *stream << "Max value = " << *maxValue << "\n";
                                                                                                numOfValue = numOfValue + 1;
                                                                                        }
                                                                                        else if (inst->getPredicate() == 36 || inst->getPredicate() == 40)
                                                                                        {
                                                                                //errs() << "Range is >= " << *i.getOperand(1)  << "\n";
                                                                                                Value* minValue = i.getOperand(1);
                                                                                                errs() << "Min value is: " << *minValue << "\n";
                                                                                                *stream << "Min value = " << *minValue << "\n";
                                                                                                numOfValue = numOfValue + 1;
                                                                                                //errs() << numOfValue << "\n";
                                                                                        }
                                                                                        else if (inst->getPredicate() == 37 || inst->getPredicate() == 41 || inst->getPredicate() == 4)
												{
                                                                                                Value* minValue = i.getOperand(1);
                                                                                                errs() << "Min value is : " << *i.getOperand(1)  << "+ 1" << "\n";
                                                                                                *stream << "Min value = " << *minValue << "+ 1" << "\n";
												numOfValue = numOfValue + 1;
                                                                                        }
                                                                                //}
                                                                        }
                                                                }
                                                        }
                                                }
                                        }
                                }
                        }
                }
        //}
	//errs() << "out of data range function" << "\n";
	}
}



//for inter-procedural pass
void TaintAnalysis::functionProcess (Function& F, Instruction* line_no1)
{
	if (&F != NULL)
	{
		//errs() << F.getName() << "\n";
	//Instruction &line_no2 = dyn_cast<Instruction>(*line_no1);
	//if (!F.hasExternalLinkage()){
	//	if (!F.isIntrinsic ()){
			//errs() << F.getName() << "\n";
			//if (depth < 100){
			for (auto& B : F) {
				for (auto& I : B) {
					visit(I, line_no1);
                		}
        		}
			//depth++;
			//}
	//	}
	//}
	}
	
}

//for main function process (it comes under externalLinkage)
void TaintAnalysis::mainfunctionProcess(Function& F, Instruction* line_no1)
{
	errs() << "inside main function" << "\n";
	for (auto& B : F) {
		for (auto& I : B) {
			visit(I, line_no1);
			if (depth > 97){
				errs() << depth << "\n";
				break;
			}
			//errs() << F.getName() << ":" << I << "\n"; 
			}
		if (depth > 50){
                          break;}
	}
}


//For each instruction, decides the type of the instruction and sends to relevant functions
void TaintAnalysis::visit(Instruction &I, Instruction*	line_no1)
{
	//errs() << I << "\n";;
	unsigned opcode = I.getOpcode();
        if (opcode == llvm::Instruction::Store)
        {
                TaintAnalysis::taintStore(I, taintMap, line_no1);
        }
	else if (opcode == llvm::Instruction::Call)
        {
                taintCallInst(I, taintMap, line_no1);
        }
        else if (opcode == llvm::Instruction::Load)
        {
                taintLoad(I, taintMap, line_no1);
        }
        else if (opcode == llvm::Instruction::ICmp)
        {
                taintIcmp(I, taintMap, line_no1);
        }
        else if (opcode == llvm::Instruction::FCmp)
        {
                taintFcmp(I, taintMap, line_no1);
        }
        else if (opcode == llvm::Instruction::GetElementPtr)
        {
                taintGetElementPtr(I, taintMap, line_no1);
        }
        else if (opcode == llvm::Instruction::Select)
        {
                taintSelect(I, taintMap, line_no1);
        }
        else if ((opcode == llvm::Instruction::And) || (opcode == llvm::Instruction::Or) || (opcode == llvm::Instruction::Xor)
                        || (opcode == llvm::Instruction::Shl) || (opcode == llvm::Instruction::LShr) || (opcode == llvm::Instruction::AShr))
        {
                taintBinaryOperator(I, taintMap, line_no1);
        }
        else if ((opcode == llvm::Instruction::Add) || (opcode == llvm::Instruction::FAdd) || (opcode == llvm::Instruction::Sub)
                        || (opcode == llvm::Instruction::FSub) || (opcode == llvm::Instruction::Mul) || (opcode == llvm::Instruction::FMul)
                        || (opcode == llvm::Instruction::UDiv) || (opcode == llvm::Instruction::SDiv) || (opcode == llvm::Instruction::FDiv)
                        || (opcode == llvm::Instruction::URem) || (opcode == llvm::Instruction::SRem) || (opcode == llvm::Instruction::FRem))
        {
                taintBinaryOperator(I, taintMap, line_no1);
        }
        else if ((opcode == llvm::Instruction::SExt) || (opcode == llvm::Instruction::Trunc) || (opcode == llvm::Instruction::ZExt))
        {
                taintConversion(I, taintMap, line_no1);
        }
        else if (opcode == llvm::Instruction::Br)
        {
                taintBr(I, taintMap, line_no1);
        }
        else if (opcode == llvm::Instruction::PHI)
        {
                taintPhi(I, taintMap, line_no1);
        }
	else
		return;
}

bool InterProPass::runOnModule(Module& m) {
	//taking file name to write the taint traces
	if (infile_file){
        	std::getline(infile_file, line_file);
		errs() << "found line_file file" << "\n";
	}
	else{
        	line_file = "taint_trace";
		errs() << "line file is trace file" << "\n";
	}
	llvm::raw_fd_ostream file(line_file, EC, F_None);

	//taking function name as input
	char *Filename_func = "function_name";
	std::ifstream infile(Filename_func);
	std::string line;
	std::getline(infile, line);
	const char* function_name;
	if (!line.empty())
	{
		function_name = line.c_str();
	}
	else{
		function_name = "PRS";
	}

	errs() << "inside runOn module" << "\n";
	int flag1 = 0;

	//taking variable name as input
	char *Filename_var = "variable";
	std::ifstream infile_var(Filename_var);
	std::string line_var;
	std::getline(infile_var, line_var);
	const char* name_var;
	if (!line_var.empty())
	{
		name_var = line_var.c_str();
		errs() << "name of the var:" << name_var << "\n";
	}
	else
	{
		errs() << "No variable name specified, cannot proceed with the Taint Analysis" << "\n";
		exit(0);
	}
	infile.close();

for(auto& F : m){
	if (F.getName() == function_name){
		errs() << "got the function from file" << "\n";
		//	if (F.getName() == "main"){
//				errs() << "Hello from: "<< F.getName() << "\n";
			for (auto& B : F) {
				for (auto& I : B) {
			        	unsigned opcode = I.getOpcode();   	
					
					//for parameters that use a function to load them
					if (opcode == llvm::Instruction::Call)
                                        {
                                                CallInst* call = dyn_cast<CallInst>(&I);
                                                Function *F1 = call->getCalledFunction();
                                                if (F1 != NULL){
                                                	StringRef name = F1->getName();
							//if(name.contains("xfs_has_bigtime")){
							//if(name.contains("ext4_has_feature_resize_inode")){  //for ext4 the fn is written like this
							if(name.contains(line_var)){
							//if (name == "ext2fs_has_feature_sparse_super"){
								errs() << F.getName() << "\n";
								errs() << "string: " << name << "\n";
                                                        	Value* V = &I;
                                                        	taintMap.insert(std::pair<Value *, bool>(V, 1));
                                                        	taintInst.push({&I, NULL});

                                                	}
                                                }
					}
					

				/*	
					//for parameters that use local variables to load them and keep them in superblock
					unsigned opcode1 = I.getOpcode();
					if (opcode1 == llvm::Instruction::Load){
					Value* V = &I;
					StringRef S = V->getName();
					int flag = 0;
					std::string str;
					llvm::raw_string_ostream ss(str);
					ss << I;
					const char* string1 = ss.str().c_str();
					if (strcmp (name_var, string1) == 0)
					//if(S == "zap_log")
					{
						errs() << "its a match" << S << "\n";
						errs() << S << "\n";
						if (flag == 0)
						{
							errs() << I << "\n";
							Type* dataType = V->getType();
							if (flag1 == 0){
							errs() << *dataType << "\n";
							//file << "Data type = " << *dataType << "\n";
							flag1 = 1;
							}
							taintMap.insert(std::pair<Value *, bool>(V, 1));
							taintInst.push({&I, NULL});
							flag = 1;
						}
					}}
				*/	
					
						
					//for parameters that use global variables to load them and keep them in superblock
                                        if (opcode == llvm::Instruction::Load)
					//if (opcode == llvm::Instruction::GetElementPtr)
                                        {
                                                Value *op1 = I.getOperand(0);
                                                Value *op2 = dyn_cast<Value>(&I);
                                                StringRef S = op1->getName();
						//errs() << S << "\n";
						if(S == name_var)
                                                //if(S == "log_name")
                                                {
                                                        //errs() << S << "\n";
							errs() << *op1 << "\n";
                                                        Type* dataType = op1->getType();
                                                        errs() << *dataType << "\n";
							file << "Data type = " << *dataType << "\n";
                                                        taintMap.insert(std::pair<Value *, bool>(op1, 1));
                                                        //taintMap.insert(std::pair<Value *, bool>(op2, 1));
                                                        taintInst.push({&I, NULL});
                                                }
                                        }
					
					
					//unsigned opcode1 = I.getOpcode();
                                        if (opcode == llvm::Instruction::Store)
                                        {
                                                Value *op1 = I.getOperand(0);
                                                Value *op2 = I.getOperand(1);
                                                StringRef S = op2->getName();
						std::string str;
                                        	llvm::raw_string_ostream ss(str);
                                        	ss << S;
                                        	const char* string1 = ss.str().c_str();
                                        	if (op2->getName() == name_var)
                                                //if(S == "blocksize")
                                                {
                                                        errs() << S << "\n";
                                                        Type* dataType = op2->getType();
                                                        errs() << *dataType << "\n";
							file << "Data type = " << *dataType << "\n";
                                                        taintMap.insert(std::pair<Value *, bool>(op2, 1));
                                                        //taintMap.insert(std::pair<Value *, bool>(op2, 1));
                                                        taintInst.push({&I, NULL});
                                                }
                                        }
                                        
					
					//for cross-component dependency, using the mapping information
                                        if (opcode == llvm::Instruction::GetElementPtr)
					{
						
						Value *op1 = dyn_cast<Value>(&I);
						StringRef S = op1->getName();
                                        	int flag = 0;
                                        	if (S.contains(line_var))
						//if(S == "sectorsize")
                                        	{
                                                	errs() << S << "\n";
                                                	if (flag == 0)
                                                	{
                                                        	//errs() << I << " : " << F.getName() << "\n";
                                                        	if (flag1 == 0){
									Type* dataType = op1->getType();
                                                        	errs() << *dataType << "\n";
                                                        	file << "Data type = " << *dataType << "\n";
                                                        	flag1 = 1;
                                                        	}
                                                        	taintMap.insert(std::pair<Value *, bool>(op1, 1));
                                                        	taintInst.push({&I, NULL});
                                                        	//flag = 1;
                                                	}
						
                                        	}
					}

						/*

					//unsigned opcode = I.getOpcode();
					if (opcode == llvm::Instruction::GetElementPtr)
					{
						int n = I.getNumOperands();
						if (n == 3)
						{
							Value *op2 = I.getOperand(2);
							//Value *op3 = I.getOperand(0);
							Value *op3 = I.getOperand(0)->stripPointerCasts();

							
                                                        std::string string1 = "6";
							//std::string string2 = string.str();
                                                        std::string string2 = op2->getNameOrAsOperand();
							//std::string string3 = op3->getNameOrAsOperand();
							//errs() << string3 << "\n";

							//ValueName* dataType = op3->getValueName();
							Type* dataType = op3->getType();
							//if ((cast<Constant>(*dataType)).isNullValue()){
								//Value st = dyn_cast<Value>(*dataType);
							//	errs() << "could be converted to stringref" << "\n";
							//}
							//std::string st = *dataType->str();
							//errs() << *dataType << "\n";
							//llvm::raw_fd_ostream file1(filename1, EC, F_None);
							//file1 << *dataType << "\n";
							std::string str;
							llvm::raw_string_ostream ss(str);
							ss << *dataType;
							const char* stringg1 = ss.str().c_str();
							
							//file1.close();
							//std::string line;
							//std::ifstream myfile( "sb_name", std::ifstream::in );
							//if (myfile){
							//	while(std::getline(myfile, line))
							//	{
							//		errs() << "line:" << line << "\n";
							//		const char* string2 = line.c_str();
							//	}
							//}
							//myfile.close();

							const char* stringg2 = "%struct.ext2_super_block*";

							if (strcmp (stringg1, stringg2) == 0)
							{
								errs() << "it's a match, line: " << stringg2 << "\n";
								if ((string1.compare(string2)) == 0){
									Value* V = &I;
									errs() << string1 << " : " << *V << "\n";
                                                                	taintMap.insert(std::pair<Value *, bool>(V, 1));
									taintInst.push({&I, NULL});
								}
							}



							
							//errs() << "before dyn cast" << "\n";
							//StructType* st1 = static_cast<StructType*>(dataType);
							//errs() << *st1 << "\n";
							//if ((*dataType).isStructTy()){
							//	errs() << "It has name" << "\n";
							//	errs() << "the name is: " << dataType->getStructName() << "\n";
							//}
							//StringRef name1 = st1->getName();
							//errs() << "printing struct name: " << name1 << "\n";
							//StructType* st = dyn_cast<StructType*>(dataType);
							//StructType *st = dyn_cast<StructType>(const_cast<Type*>(dataType));
							//dataType->dump();
							//errs() << *dataType << "\n";
							//errs() << "after dyn cast" << "\n";
							//errs() << st << "\n";
							//StringRef name = st->getName();
							//errs() << "printing struct name: " << name << "\n";
							//errs() << "printing struct type" << "\n";
							//string len = dataType->getAsString();
							//errs() << len << "\n";
							//PointerType* p = dyn_cast<PointerType>(dataType);
							//StringRef st = p->get();
							//errs() << st << "\n";
					*/
							/*if (!(dataType->getStructName().empty())){
								errs() << dataType->getStructName() << "\n";
							}

                                                        if ((string1.compare(string2)) == 0)
                                                        {
								//errs() << I << "\n";
                                                                Value* V = &I;
                                                                //Type* dataType = V->getType();
                                                                //errs() << "Data type = " <<*dataType << "\n";
                                                                taintMap.insert(std::pair<Value *, bool>(V, 1));
                                                                taintInst.push({&I, NULL});

                                                        }*/
                                        //        }
			//		} //end of getelementptr
        //                                }
					
				}
				}
//			}
		}
	}

        for(auto& F : m){
                if (F.getName() == function_name){
                        errs() << "Hello from: "<< F.getName() << "\n";
	//		depth = 0;
			TaintAnalysis::functionProcess(F, NULL);
			//TaintAnalysis::printInst(taintInst, m);
			//file.close();
                }
	}
	TaintAnalysis::printInst(taintInst, m);
//	file.close();
//	}
//		}
	//	errs() << "end of analysis2" << "\n";
	//}
	return false;
}

}
//Registers the pass, pass name is "interpro", library is libSkeletonPass.so
char StaticAnalysis::InterProPass::ID = 0;
static RegisterPass<StaticAnalysis::InterProPass> SCCReg("interpro", "InterPro Pass");

