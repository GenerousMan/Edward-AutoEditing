<template>
    <div class="loading">
        <div class="box">
            <div class="gif"><img src="@/assets/loading.gif"/></div>
            <div class="msg">{{msg}}</div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Loading',
    props: ['msg']
}
</script>

<style scoped>
.loading {
    position: fixed;
    top: 0px;
    left: 0px;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(10px);
    z-index: 99;
}

.box {
    position: absolute;
    top: 50%;
    left: 50%;
    margin-left: -200px;
    margin-top: -120px;
    width: 400px;
    height: 200px;
    text-align: center;
    border-radius: 8px;
    background: rgb(236, 240, 241);
}

.gif {
    margin-top: 12px;
    height: 120px;
}

.gif img {
    height: 100%;
}

.msg {
    font-size: 20px;
    font-weight: bold;
    color: rgb(27, 27, 27);
}
</style>