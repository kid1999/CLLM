<template>
  <div class="home">
    <div class="content_box">
      <div class="title_box">
        <div class="right_icon" @click="toggleBox">
          <i class="el-icon-caret-right" v-if="isCollaspe"></i>
          <i class="el-icon-caret-left" v-else></i>
        </div>
        <h1>LLM FOR BLOCKCHAIN</h1>
      </div>
      <div class="content">
        <div class="request_box">
          <el-form ref="form" :model="form" :rules="rules" label-width="150px">
            <el-form-item label="Contract Adress" prop="addr">
              <el-input v-model="form.addr"></el-input>
            </el-form-item>
            <el-form-item label="Question" prop="qes">
              <el-input
                v-model="form.qes"
                placeholder="Please input your question"
              ></el-input>
            </el-form-item>
            <el-form-item label="LLM" prop="region">
              <el-select
                v-model="form.region"
                placeholder="Please select a large model node"
                style="width: 100%"
              >
                <el-option label="ChatGPT" value="chatgpt"></el-option>
                <el-option label="Hunyuan" value="hunyuan"></el-option>
                <el-option label="Gemini" value="gemini"></el-option>
                <el-option label="Llama" value="llama"></el-option>
                <el-option label="ChatGLM" value="chatglm"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit" :loading="isLoading"
                >Search</el-button
              >
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
    <div class="anwser_box" ref="anwser_box" id="anwser_box" v-loading="isAnwserLoading">
      <div class="anwer_q" style="color: #0f8de9">{{ anwserQuestion }}</div>
      <div class="anwer_c">{{ anwserContent }}</div>
    </div>
  </div>
</template>

<script>
import { ethers } from "ethers";
import {
  contractABI,
  contractAddress,
  PRIVATEKEY,
} from "../contractABI/userContract.js";
export default {
  name: "HomeView",
  data() {
    return {
      requestID: "",
      isLoading: false, //按钮加载
      isCollaspe: true, //折叠框
      anwserContent: "", //答案内容
      anwserQuestion: "", //问题
      isAnwserLoading:true,//问题loading
      form: {
        addr: contractAddress,
        qes: "",
        region: "",
      }, //表单数据
      userInfo: {
        balance: "",
        address: "",
      }, //钱包数据
      rules: {
        addr: [
          {
            required: true,
            message: "Please enter the contract address",
            trigger: "blur",
          },
        ],
        qes: [
          {
            required: true,
            message: "Please enter the query content",
            trigger: "blur",
          },
        ],
        region: [
          { required: true, message: "Please select a node", trigger: "blur" },
        ],
      },
    };
  },
  mounted() {
    this.$refs["anwser_box"].style.width = "0px";
  },
  methods: {
    //链接区块链
    Provider() {
      let provider;
      if (window.ethereum == null) {
        console.log("MetaMask not installed; using read-only defaults");
        provider = ethers.getDefaultProvider();
      } else {
        provider = new ethers.BrowserProvider(window.ethereum);
      }
      return provider;
    },

    //合约类实例
    async Contract() {
      const provider = this.Provider();
      const signer = await provider.getSigner();
      const contract = new ethers.Contract(
        contractAddress,
        contractABI,
        signer
      );
      return contract;
    },

    // 登录钱包
    async checkLogin() {
      const provider = this.Provider();
      const wallet = new ethers.Wallet(PRIVATEKEY, provider);
      const balance = await provider.getBalance(wallet.address);
      this.userInfo.balance = ethers.formatEther(balance);
      this.userInfo.address = wallet.address;
    },

    //搜索
    async onSubmit() {
      this.$refs["form"].validate(async (valid) => {
        if (valid) {
          this.checkLogin();
          this.isLoading = true;
          const contract = await this.Contract();
          const tx = await contract.requestLLM(this.form.qes, this.form.region);
          const receipt = await tx.wait();
          const logs = receipt.logs.map((log) =>
            contract.interface.parseLog(log)
          );
          this.requestID = Number(logs[1].args[0]);
          this.isLoading = false;
          await this.getOracleResult();
          if (this.isCollaspe) {
            this.toggleBox();
          }
        }
      });
    },

    //根据requestID获取结果
    async getOracleResult() {
      this.isAnwserLoading=true;
      this.anwserQuestion = "";
      this.anwserContent = "";
      const contract = await this.Contract();
      const myEventFilter = contract.filters.ReturnResult();
      const myEventListener = contract.on(myEventFilter, (event) => {
        this.isAnwserLoading=false;
        this.anwserQuestion = this.form.qes;
        this.anwserContent = event.args[1];
      })
    },

    //答案框
    toggleBox() {
      this.isCollaspe = !this.isCollaspe;
      if (this.isCollaspe) {
        this.$refs["anwser_box"].style.width = 0;
      } else {
        this.$refs["anwser_box"].style.width = "400px";
      }
    },
  },
};
</script>
<style lang='scss'>
.home {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.content_box {
  padding: 10px;
  width: 650px;
  height: 320px;
  background-color: white;
}
.anwser_box {
  width: 400px;
  height: 340px;
  background-color: white;
  transition: width 0.28s;
  overflow: hidden;
  .anwer_q {
    display: flex;
    justify-content: flex-start;
    border-bottom: 1px solid gray;
    padding-top: 9px;
    padding-bottom: 5px;
    font-size: 18px;
    overflow: hidden;
  }
  .anwer_c {
    display: flex;
    justify-content: flex-start;
    padding-top: 10px;
    padding-bottom: 5px;
    padding-right: 5px;
    max-height: 280px;
    overflow: auto;
  }
}
.right_icon {
  display: flex;
  justify-content: flex-end;
  cursor: pointer;
}
.content {
  margin: 10px;
}
</style>